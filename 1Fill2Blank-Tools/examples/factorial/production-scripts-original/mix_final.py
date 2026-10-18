"""Place voice clips at final marks, duck music under voice, mux final MP4."""
import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/home/user")
PROD = ROOT / "production"
VIDEO = PROD / "media_pass1/videos/factorial_production/1080p30/FactrioalScene.mp4"
MARKS = json.loads((PROD / "marks_final.json").read_text())
VDUR = json.loads((PROD / "voice_durations.json").read_text())
OUT = ROOT / "Factorial_1Fill2Blank_FINAL.mp4"
VOICE_TRACK = PROD / "voice_track.wav"
MUSIC = PROD / "music.wav"
SEGS = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"]
ORDER = ["S01", "S02", "LOGO_MID", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "OUTRO", "END"]


def run(cmd):
    print("+", " ".join(str(c) for c in cmd)[:300])
    subprocess.run([str(c) for c in cmd], check=True)


def duration(path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)], text=True)
    return float(json.loads(out)["format"]["duration"])


def mean_volume_db(path) -> float:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", p.stderr)
    if not m:
        sys.exit(f"volumedetect failed for {path}")
    return float(m.group(1))


def main() -> None:
    video_dur = duration(VIDEO)
    # sync sanity table
    plan = []
    print(f"{'seg':5s} {'start':>8s} {'end':>8s} {'next':>8s} {'gap':>6s}")
    for k in SEGS:
        start = float(MARKS[k])
        end = start + float(VDUR[k])
        nxt_key = ORDER[ORDER.index(k) + 1]
        nxt = float(MARKS[nxt_key])
        plan.append({"seg": k, "voice_start_s": round(start, 3), "voice_end_s": round(end, 3),
                     "next_segment_start_s": round(nxt, 3), "gap_s": round(nxt - end, 3)})
        print(f"{k:5s} {start:8.2f} {end:8.2f} {nxt:8.2f} {nxt - end:6.2f}")
        if end > nxt + 0.05:
            sys.exit(f"OVERLAP: {k} ends {end:.2f} after next segment {nxt:.2f}")
    (PROD / "sync_plan.json").write_text(json.dumps(plan, indent=2))

    # 1) voice track: each clip delayed to its mark
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for k in SEGS:
        cmd += ["-i", str(PROD / "audio" / f"{k}.mp3")]
    filters = []
    labels = []
    for i, k in enumerate(SEGS):
        ms = int(round(float(MARKS[k]) * 1000))
        filters.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,adelay={ms}|{ms}[v{i}]")
        labels.append(f"[v{i}]")
    filters.append("".join(labels) + f"amix=inputs={len(SEGS)}:duration=longest:dropout_transition=0:normalize=0[mix]")
    filters.append(f"[mix]apad=whole_dur={video_dur:.3f},atrim=0:{video_dur:.3f}[vout]")
    cmd += ["-filter_complex", ";".join(filters), "-map", "[vout]", "-c:a", "pcm_s16le", str(VOICE_TRACK)]
    run(cmd)

    # 2) pick music level: unducked mean ~11 dB below voice mean (sidechain ducks it further while speaking)
    voice_mean = mean_volume_db(VOICE_TRACK)
    music_mean = mean_volume_db(MUSIC)
    gain_db = (voice_mean - 11.0) - music_mean
    gain = 10 ** (gain_db / 20.0)
    gain = min(1.0, max(0.05, gain))
    print(f"voice mean {voice_mean:.1f} dB | music mean {music_mean:.1f} dB | music gain {gain:.3f} ({20*math.log10(gain):+.1f} dB)")

    # 3) final mux: video copied, music ducked by voice, gentle loudnorm for YouTube
    fc = (
        "[1:a]asplit=2[vm][vsc];"
        f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.4f}[mus];"
        "[mus][vsc]sidechaincompress=threshold=0.02:ratio=6:attack=150:release=850:makeup=1[duck];"
        "[vm][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        "loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[aout]"
    )
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(VIDEO), "-i", str(VOICE_TRACK), "-i", str(MUSIC),
         "-filter_complex", fc, "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", "-t", f"{video_dur:.3f}", str(OUT)])
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
