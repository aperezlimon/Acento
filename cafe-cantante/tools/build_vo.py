#!/usr/bin/env python3
"""Build the narration track and its timing map from assets/audio/vo/guion.txt.

Each scene line is split into phrases; every phrase is synthesised (Kokoro by
default, or Piper) so its start and end on the timeline are exact (they drive
captions and cues). Phrases are cached, so a rebuild keeps the same audio.

Output:
  assets/audio/narration.wav   the whole voice track, scenes placed on the timeline
  timings.json                 scenes and phrases with start/end in seconds

Usage: python3 tools/build_vo.py [--engine kokoro|piper] [--voice ef_dora] [--speed 0.92]
"""
import argparse
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR = 24000  # set per engine in main()

# Per scene: silence before the voice starts, and hold after it ends (seconds).
LEAD = [0.2, 0.3, 1.2, 0.3, 0.3, 0.3, 0.8, 0.3, 0.5]
TAIL = [0.5, 0.4, 0.4, 0.4, 1.1, 0.4, 0.5, 1.4, 2.8]
GAP_COMMA, GAP_STOP = 0.16, 0.32


def phrases(line):
    parts = [p.strip() for p in re.findall(r"[^,.:;…]+[,.:;…]*", line) if p.strip()]
    out = []
    for p in parts:
        if out and len(p.split()) < 3:
            out[-1] += " " + p
        else:
            out.append(p)
    # Merge a too-short first phrase forward.
    if len(out) > 1 and len(out[0].split()) < 3:
        out[1] = out[0] + " " + out[1]
        out.pop(0)
    return out


CACHE = ROOT / "assets/audio/vo/phrases"


_KOKORO = None
KOKORO_DIR = Path.home() / ".cache/hyperframes/tts"


def synth_kokoro(text, voice, speed):
    """Kokoro-82M via kokoro_onnx (the model hyperframes tts downloads)."""
    global _KOKORO
    import hashlib
    import numpy as np
    key = hashlib.sha1(f"kokoro|{voice}|{speed}|{text}".encode()).hexdigest()[:16]
    cached = CACHE / f"{key}.wav"
    if not cached.exists():
        if _KOKORO is None:
            from kokoro_onnx import Kokoro
            _KOKORO = Kokoro(str(KOKORO_DIR / "models/kokoro-v1.0.onnx"), str(KOKORO_DIR / "voices/voices-v1.0.bin"))
        audio, sr = _KOKORO.create(text, voice=voice, speed=speed, lang="es")
        assert sr == SR, sr
        pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
        CACHE.mkdir(parents=True, exist_ok=True)
        with wave.open(str(cached), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)
    with wave.open(str(cached)) as w:
        return w.readframes(w.getnframes())


def synth(text, model, ls, dest):
    """Piper is not deterministic, so each phrase is synthesised once and cached."""
    import hashlib
    key = hashlib.sha1(f"{Path(model).name}|{ls}|{text}".encode()).hexdigest()[:16]
    cached = CACHE / f"{key}.wav"
    if cached.exists():
        with wave.open(str(cached)) as w:
            return w.readframes(w.getnframes())
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = cached
    subprocess.run(
        ["python3", "-m", "piper", "-m", model, "--length-scale", str(ls),
         "--sentence-silence", "0", "-f", str(dest)],
        input=text.encode(), check=True, capture_output=True)
    with wave.open(str(dest)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return w.readframes(w.getnframes())


def trim(pcm, thresh=250):
    """Strip leading/trailing near-silence (16-bit mono)."""
    import array
    a = array.array("h", pcm)
    win = int(SR * 0.01)
    def loud(i):
        seg = a[i:i + win]
        return seg and max(abs(x) for x in seg) > thresh
    s = 0
    while s < len(a) and not loud(s):
        s += win
    e = len(a)
    while e > s and not loud(max(s, e - win)):
        e -= win
    s = max(0, s - int(SR * 0.03))
    e = min(len(a), e + int(SR * 0.06))
    return a[s:e].tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=str(Path.home() / ".cache/piper/es_ES-davefx-medium.onnx"))
    ap.add_argument("--length-scale", type=float, default=1.22)
    ap.add_argument("--engine", choices=["kokoro", "piper"], default="kokoro")
    ap.add_argument("--voice", default="ef_dora")
    ap.add_argument("--speed", type=float, default=0.92)
    args = ap.parse_args()
    global SR
    SR = 24000 if args.engine == "kokoro" else 22050

    lines = [l.strip() for l in (ROOT / "assets/audio/vo/guion.txt").read_text().splitlines() if l.strip()]
    assert len(lines) == len(LEAD), f"{len(lines)} lines, {len(LEAD)} scenes"
    track = bytearray()
    t = 0.0
    scenes = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, line in enumerate(lines):
            start = t
            track += b"\0\0" * int(LEAD[i] * SR)
            t += LEAD[i]
            ph = []
            for j, p in enumerate(phrases(line)):
                if args.engine == "kokoro":
                    raw = synth_kokoro(p, args.voice, args.speed)
                else:
                    raw = synth(p, args.model, args.length_scale, Path(tmp) / f"{i}_{j}.wav")
                pcm = trim(raw)
                d = len(pcm) / 2 / SR
                ph.append({"text": p, "start": round(t, 3), "end": round(t + d, 3)})
                track += pcm
                t += d
                gap = GAP_STOP if p[-1] in ".:…" else GAP_COMMA
                track += b"\0\0" * int(gap * SR)
                t += gap
            t = ph[-1]["end"] + TAIL[i]
            track = track[: int(t * SR) * 2]
            track += b"\0\0" * (int(t * SR) - len(track) // 2)
            scenes.append({"id": f"s{i+1}", "start": round(start, 3), "end": round(t, 3),
                           "vo_start": ph[0]["start"], "vo_end": ph[-1]["end"], "phrases": ph})
    out = ROOT / "assets/audio/narration.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(bytes(track))
    (ROOT / "timings.json").write_text(json.dumps({"duration": round(t, 3), "scenes": scenes},
                                                  ensure_ascii=False, indent=1))
    print(f"narration {t:.2f}s, {len(scenes)} scenes")
    for s in scenes:
        print(s["id"], s["start"], s["end"], len(s["phrases"]), "phrases")


if __name__ == "__main__":
    main()
