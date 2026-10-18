"""Original 3Blue1Brown-STYLE background music (not any existing track).

Slow, contemplative, minimal piano arpeggios + soft pad + sparse melody,
synthesised note-by-note with numpy. Usage: make_music.py <seconds> <out.wav>
"""
import math
import random
import sys
import wave

import numpy as np

SR = 44100


def f(midi: float) -> float:
    return 440.0 * 2.0 ** ((midi - 69.0) / 12.0)


def add_tone(buf, start_s, midi, dur, vel, pan=0.0, kind="piano"):
    n0 = int(start_s * SR)
    n = int(dur * SR)
    if n0 >= buf.shape[1]:
        return
    n = min(n, buf.shape[1] - n0)
    if n <= 0:
        return
    t = np.arange(n, dtype=np.float32) / SR
    freq = f(midi)
    if kind == "piano":
        sig = np.zeros(n, dtype=np.float32)
        for k, amp in enumerate([1.0, 0.48, 0.23, 0.11, 0.05, 0.02], start=1):
            sig += amp * np.sin(2 * np.pi * freq * k * t, dtype=np.float32) * np.exp(-t * (1.6 + 0.8 * k))
        sig *= (1.0 - np.exp(-t * 250.0)) * vel
    elif kind == "pad":
        env = np.minimum(1.0, np.minimum(t / 1.2, np.maximum(0.0, (dur - t) / 1.2)))
        trem = 0.92 + 0.08 * np.sin(2 * np.pi * 0.07 * t + midi)
        sig = (np.sin(2 * np.pi * freq * t) + 0.30 * np.sin(2 * np.pi * freq * 2 * t)) * env * trem * vel
    else:  # bass
        env = np.minimum(1.0, np.minimum(t / 0.08, np.maximum(0.0, (dur - t) / 0.4)))
        sig = (np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(2 * np.pi * freq * 2 * t)) * env * np.exp(-t * 0.25) * vel
    left = math.cos((pan + 1.0) * math.pi / 4.0)
    right = math.sin((pan + 1.0) * math.pi / 4.0)
    buf[0, n0:n0 + n] += sig * left
    buf[1, n0:n0 + n] += sig * right


def main() -> None:
    duration = float(sys.argv[1])
    out = sys.argv[2]
    rng = random.Random(7)
    total = int(duration * SR)
    buf = np.zeros((2, total), dtype=np.float32)

    bpm = 72.0
    beat = 60.0 / bpm
    bar = 4 * beat
    # chord: (bass midi, pad/arp midi tones low->high)
    prog = [
        (45, [57, 59, 60, 64, 69]),   # Am(add9)
        (41, [53, 57, 60, 64, 69]),   # Fmaj7
        (36, [55, 59, 60, 64, 67]),   # Cmaj7
        (43, [55, 59, 62, 64, 67]),   # G6
        (45, [57, 59, 60, 64, 69]),   # Am(add9)
        (41, [53, 57, 60, 65, 69]),   # Fmaj9-ish
        (40, [52, 55, 59, 62, 64]),   # Em7
        (43, [55, 59, 62, 67, 71]),   # G
    ]
    melody_pool = [69, 72, 76, 74, 72, 69, 67, 64, 67, 72, 71, 69, 67, 64, 62, 64]
    melody_idx = 0
    nbars = int(math.ceil(duration / bar))
    for b in range(nbars):
        t0 = b * bar
        bass, tones = prog[b % len(prog)]
        # bass + pad chord for the whole bar
        add_tone(buf, t0, bass, bar * 1.05, 0.16, pan=0.0, kind="bass")
        for j, m in enumerate(tones[:4]):
            add_tone(buf, t0, m, bar * 1.05, 0.038, pan=-0.25 + 0.16 * j, kind="pad")
        # gentle arpeggio: 8th notes cycling the chord tones
        for step in range(8):
            tt = t0 + step * (beat / 2) + rng.uniform(-0.02, 0.02)
            if tt < 1.0 or tt > duration - 3.0:
                continue
            m = tones[(step * 2 + b) % len(tones)]
            add_tone(buf, tt, m + 12, 2.4, 0.055 * rng.uniform(0.8, 1.15),
                     pan=rng.uniform(-0.3, 0.3), kind="piano")
        # sparse melody, roughly every other bar
        if b >= 2 and b % 2 == 0 and t0 < duration - 8:
            for beat_i in (0, 2):
                m = melody_pool[melody_idx % len(melody_pool)]
                melody_idx += 1
                add_tone(buf, t0 + beat_i * beat + rng.uniform(0, 0.05), m + 12, 3.2,
                         0.075, pan=rng.uniform(-0.15, 0.15), kind="piano")

    # fake small-room reverb: a few quiet echoes
    wet = buf.copy()
    for delay_s, gain in [(0.11, 0.22), (0.23, 0.14), (0.39, 0.08), (0.57, 0.05)]:
        d = int(delay_s * SR)
        wet[:, d:] += buf[:, :-d] * gain
    buf = wet

    # master fades + peak normalise to 0.62
    fade_in = int(2.5 * SR)
    fade_out = int(5.0 * SR)
    buf[:, :fade_in] *= np.linspace(0, 1, fade_in, dtype=np.float32)
    buf[:, -fade_out:] *= np.linspace(1, 0, fade_out, dtype=np.float32) ** 1.5
    peak = float(np.max(np.abs(buf))) or 1.0
    buf *= (0.62 / peak)

    pcm = (np.clip(buf, -1, 1) * 32767).astype(np.int16).T  # (samples, 2)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"WROTE {out}  {duration:.1f}s  peak_in={peak:.3f}")


if __name__ == "__main__":
    main()
