# Factorial — 1Fill2Blank production notes

## Final deliverable
- `Factorial_1Fill2Blank_FINAL.mp4` — 1920x1080, 30fps, H.264 + AAC 192k stereo 48kHz, 03:41.6, ~13MB
- Loudness: -15.8 LUFS integrated, true peak -1.2 dBFS (loudnorm I=-15 in the mix)

## Inputs used
- Scene: repo `1Fill2Blank/year2026/factorial/factorial_scene.py` (FactrioalScene, ManimCE)
  via generated `factorial_production.py` — adds ONLY: mid/outro logo (repo `Logo1Fill2Blank`
  explode-assemble, as in the pasted version), sync marks and voice-length holds. No visual
  logic/design changed (on-screen tree label stays "Combination Tree", equation order kept).
- Voice script: the user's FINAL timed script pasted in chat (supersedes repo `script.tex`).
  Spoken text with formulas verbalised is in `narration_segments.json`; 12 script windows were
  merged into 9 clips (`audio/S01.mp3` … `S09.mp3`, selected male Bengali voice).
  Typo fixed: split word সমস্যা/র -> সমস্যার.
- Music: ORIGINAL track generated in code (`make_music.py`, `music.mp3`) — slow contemplative
  piano arpeggio + pad in a 3Blue1Brown *style*; not any existing/copyrighted track.
  Mixed ~11 dB below voice level and sidechain-ducked under narration. Logo parts are music-only.
- Setup: `manim-sandbox-setup` repo — `manimce.sh` (ManimCE 0.21.0, CMU Serif + Noto Serif
  Bengali via `font.sh`) + `latex_slim.sh`. Verified: pip check clean, font.sh --check OK,
  FontsOnly + FontsAndMath examples rendered.

## Sync method (two passes)
1. Pass 1 (480p15, no pads) recorded scene-time marks; total 02:48.7 — matching the script's
   02:49 windows almost exactly (S02 at 11.0s, players at 43.8s, etc.).
2. Voice total is 03:13.9, longer than the script windows allow (e.g. football intro needs
   11.9s vs the 7s window; the n-generalisation needs 42.3s vs 31.2s of animation).
   So each segment got a static hold (`pad.json`, total +53.0s) where the relevant finished
   visual stays on screen. S07's 18.6s hold sits BEFORE the equation assembles, over the
   complete tree + six arrangements, because the narration is still describing those there.
3. Pass 2 (1080p30, with pads) re-recorded marks; voice clips were delayed to those marks.
   Every clip ends before the next segment starts (gaps 0.23s–1.36s, see `sync_plan.json`).

## Final timeline (voice starts)
| Time  | Segment |
|-------|---------|
| 00:00 | S01 Opening formulas (Binomial / Taylor / Combinations) |
| 00:11 | S02 Big "!", 1!–20! list, n! formula, "?" marks |
| ~00:33–00:45 | Logo (music only) |
| 00:45 | S03 Football intro — A, B, C / GK, DF, ST |
| 00:57 | S04 Swaps + "তিনজনকে মোট কতভাবে সাজানো যায়?" |
| 01:18 | S05 Three blocks — choices 3, 2, 1 |
| 01:44 | S06 Combination Tree builds |
| 02:03 | S07 Six paths highlighted, 3×2×1 = 6, 3! equation |
| 02:41 | S08 General case n, (n-1), (n-2), … final n! equation |
| 03:23 | S09 Closing line over final equation |
| 03:31–03:42 | Outro logo (music only) |

## QC performed
- Full decode of final MP4: OK. Streams/duration verified with ffprobe.
- No silence >3s below -45 dB anywhere (music fills all gaps/logos).
- Spot levels: voice windows ≈ -18.5 dB mean; logo/music-only windows ≈ -25…-27 dB mean.
- Frames checked visually at 8 timestamps (`thumbs/contact_sheet.jpg`).

## Kept for revisions
- `audio/S01-S09.mp3` (individual voice clips), `voice_track.mp3`, `music.mp3`
- `FactrioalScene_silent_1080p30.mp4` (rendered video before audio mix)
- `marks_pass1.json`, `marks_final.json`, `pad.json`, `sync_plan.json`, `voice_durations.json`
- Scripts: `make_production_scene.py`, `compute_pads.py`, `make_music.py`, `mix_final.py`
- Note for a future sandbox session: system packages and `.venv` do not persist — rerun
  `bash manimce.sh && bash latex_slim.sh` in `manim-sandbox-setup/` before re-rendering
  (fonts in `manim-sandbox-setup/fonts/` persist). Possible refinements if wanted:
  speed the whole voice up slightly instead of holds, split S07/S08 holds across their
  internal stages, add subtitles, or render 1080p60.
