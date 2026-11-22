#!/usr/bin/env python3
"""Build the narration track and its timing map from assets/audio/vo/guion.txt.

Each scene line is split into phrases; every phrase is synthesised with Piper
so its start and end on the timeline are exact (they drive captions and cues).

Output:
  assets/audio/narration.wav   the whole voice track, scenes placed on the timeline
  timings.json                 scenes and phrases with start/end in seconds

Usage: python3 tools/build_vo.py [--model PATH] [--length-scale 1.22]
"""
import argparse
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR = 22050

# Per scene: silence before the voice starts, and hold after it ends (seconds).
LEAD = [0.3, 0.4, 3.0, 0.5, 1.2, 0.6, 2.6, 0.6, 0.8]
TAIL = [0.9, 0.8, 0.5, 0.6, 2.0, 0.6, 0.6, 3.6, 4.5]
GAP_COMMA, GAP_STOP = 0.22, 0.42


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
    args = ap.parse_args()

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
                pcm = trim(synth(p, args.model, args.length_scale, Path(tmp) / f"{i}_{j}.wav"))
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
