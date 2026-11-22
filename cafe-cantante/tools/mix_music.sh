#!/usr/bin/env bash
# Build the music bed: El Mochuelo's soleares under the narration, ducked
# whenever the voice speaks, so it rises in the breaths (the door, the map,
# the empty chair) and in the closing hold. Palmas sit under the café scenes.
#
# Inputs (assets/audio): mochuelo-soleares-src.wav, optional palmas-src.ogg,
#                        narration.wav, and timings.json for scene times.
# Output: assets/audio/musica.wav (same length as the film).
set -euo pipefail
cd "$(dirname "$0")/.."
A=assets/audio
DUR=$(python3 -I -c "import json;print(json.load(open('timings.json'))['duration'])")
# Scene starts for the palmas window (s3 to the end of s6).
read P0 P1 < <(python3 -I -c "
import json;s={x['id']:x for x in json.load(open('timings.json'))['scenes']}
print(s['s3']['start'], s['s6']['end'])")
OFFSET=${MUSIC_OFFSET:-0}

PALMAS_IN=()
PALMAS_CHAIN="anullsrc=r=44100:cl=stereo,atrim=0:${DUR}[pal]"
if [ -f "$A/palmas-src.ogg" ]; then
  PALMAS_IN=(-i "$A/palmas-src.ogg")
  PALMAS_CHAIN="[2:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:$(python3 -I -c "print($P1-$P0)"),volume=0.22,afade=t=in:d=1.5,afade=t=out:st=$(python3 -I -c "print($P1-$P0-1.5)"):d=1.5,adelay=$(python3 -I -c "print(int($P0*1000))")|$(python3 -I -c "print(int($P0*1000))"),apad,atrim=0:${DUR}[pal]"
fi

ffmpeg -y -v error \
  -i "$A/mochuelo-soleares-src.wav" -i "$A/narration.wav" "${PALMAS_IN[@]}" \
  -filter_complex "
    [0:a]aresample=44100,aformat=channel_layouts=stereo,atrim=${OFFSET}:$(python3 -I -c "print($OFFSET+$DUR)"),asetpts=N/SR/TB,
         highpass=f=90,loudnorm=I=-20:TP=-3:LRA=11,volume=0.9,
         afade=t=in:d=1.2,afade=t=out:st=$(python3 -I -c "print($DUR-3)"):d=3[mus];
    [1:a]aresample=44100,aformat=channel_layouts=stereo,apad,atrim=0:${DUR}[vo];
    ${PALMAS_CHAIN};
    [mus][pal]amix=inputs=2:normalize=0[bed];
    [bed][vo]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=650:makeup=1[duck];
    [duck]atrim=0:${DUR}[out]" \
  -map "[out]" -ar 44100 "$A/musica.wav"
echo "wrote $A/musica.wav ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$A/musica.wav") s)"
