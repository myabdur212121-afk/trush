"""Measure voice clip durations + pass-1 segment lengths -> pad.json.

pad[K] = extra hold (seconds) to insert at the end of segment K so the
voice clip for K finishes (>=0.45s gap) before the next segment starts.
Usage: compute_pads.py <marks.json> <audio_dir> <out_pad.json>
"""
import json
import pathlib
import subprocess
import sys

ORDER = ["S01", "S02", "LOGO_MID", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "OUTRO", "END"]
VOICE = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"]
GAP = 0.45


def dur(path: pathlib.Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)], text=True)
    return float(json.loads(out)["format"]["duration"])


def main() -> None:
    marks = json.loads(pathlib.Path(sys.argv[1]).read_text())
    audio = pathlib.Path(sys.argv[2])
    missing = [k for k in ORDER if k not in marks]
    if missing:
        sys.exit(f"MISSING MARKS: {missing}  (got {list(marks)})")
    starts = {k: float(marks[k]) for k in ORDER}
    if any(starts[ORDER[i + 1]] < starts[ORDER[i]] - 1e-6 for i in range(len(ORDER) - 1)):
        sys.exit(f"MARKS NOT MONOTONIC: {starts}")

    voice_dur = {}
    for k in VOICE:
        p = audio / f"{k}.mp3"
        if not p.exists():
            sys.exit(f"MISSING AUDIO {p}")
        voice_dur[k] = dur(p)

    pads = {}
    print(f"{'seg':9s} {'start':>8s} {'anim_len':>9s} {'voice':>7s} {'pad':>7s}")
    for i, k in enumerate(ORDER[:-1]):
        anim_len = starts[ORDER[i + 1]] - starts[k]
        vale = voice_dur.get(k, 0.0)
        pad = max(0.0, vale + GAP - anim_len) if k in voice_dur else 0.0
        if k in voice_dur:
            pads[k] = round(pad, 3)
        print(f"{k:9s} {starts[k]:8.2f} {anim_len:9.2f} {vale:7.2f} {pad:7.2f}")
    print(f"{'END':9s} {starts['END']:8.2f}")
    print(f"voice total: {sum(voice_dur.values()):.2f}s   pads total: {sum(pads.values()):.2f}s   "
          f"expected final: {starts['END'] + sum(pads.values()):.2f}s")
    pathlib.Path(sys.argv[3]).write_text(json.dumps(pads, indent=2))
    pathlib.Path("/home/user/production/voice_durations.json").write_text(json.dumps(voice_dur, indent=2))
    print("WROTE", sys.argv[3])


if __name__ == "__main__":
    main()
