"""Synthesize soft, 3b1b-style ambient music cues (no external samples).
Outputs:
  audio/music_intro.wav  - opening cue (fades in, fades out slowly)
  audio/music_title.wav  - chapter-title sting (slow swell + gentle bell chord, fades away)
"""
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
import wave, pathlib

SR = 44100
OUT = pathlib.Path(__file__).parent / "audio"
rng = np.random.default_rng(7)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def piano(freq, dur, amp=0.25):
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for k, a in enumerate([1, .45, .22, .12, .06, .03], start=1):
        y += a * np.sin(2 * np.pi * freq * k * t * (1 + 0.0004 * k)) * np.exp(-t * (1.6 + 0.9 * k))
    att = np.minimum(1, t / 0.006)
    return amp * y * att


def pad(freqs, dur, amp=0.08, attack=2.5, release=3.0):
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0, 0.12):
            ff = f * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            y += np.sin(2 * np.pi * ff * t + ph) + 0.25 * np.sin(2 * np.pi * 2 * ff * t + ph)
    y /= (len(freqs) * 3)
    lfo = 1 + 0.08 * np.sin(2 * np.pi * 0.23 * t)
    env = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release).clip(0, 1)
    sos = butter(2, 1800, 'low', fs=SR, output='sos')
    return amp * sosfilt(sos, y * lfo * env)


def reverb(x, seconds=2.4, mix=0.35):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir_l = rng.standard_normal(n) * np.exp(-t * 3.2)
    ir_r = rng.standard_normal(n) * np.exp(-t * 3.2)
    sos = butter(2, 4000, 'low', fs=SR, output='sos')
    ir_l, ir_r = sosfilt(sos, ir_l), sosfilt(sos, ir_r)
    ir_l /= np.abs(ir_l).sum() ** 0.5 * 6
    ir_r /= np.abs(ir_r).sum() ** 0.5 * 6
    wl = fftconvolve(x, ir_l)[:len(x) + n]
    wr = fftconvolve(x, ir_r)[:len(x) + n]
    dry = np.pad(x, (0, n))
    L = min(len(dry), len(wl), len(wr)); dry, wl, wr = dry[:L], wl[:L], wr[:L]
    return np.stack([dry * (1 - mix) + wl * mix, dry * (1 - mix) + wr * mix], axis=1)


def place(buf, sig, at):
    i = int(at * SR)
    end = min(len(buf), i + len(sig))
    buf[i:end] += sig[:end - i]


def fade(st, fin, fout):
    n = len(st)
    t = np.arange(n) / SR
    env = np.minimum(1, t / max(fin, 1e-3))
    env *= np.clip((n / SR - t) / max(fout, 1e-3), 0, 1) ** 1.5
    return st * env[:, None]


def save(path, st, peak_db=-14):
    st = st / (np.abs(st).max() + 1e-9) * 10 ** (peak_db / 20)
    data = (st * 32767).astype(np.int16)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())
    print("wrote", path, f"{len(st)/SR:.2f}s")


def intro():
    dur = 11.0
    buf = np.zeros(int(dur * SR))
    # chords: Fmaj9 -> Am7 -> Cmaj9 (dreamy, calm)
    place(buf, pad([midi(n) for n in (41, 53, 57, 60, 64)], 5.2, amp=0.09), 0.0)
    place(buf, pad([midi(n) for n in (45, 52, 57, 60, 67)], 4.6, amp=0.09), 4.0)
    place(buf, pad([midi(n) for n in (36, 48, 55, 59, 62, 64)], 5.0, amp=0.10), 7.2)
    arp = [(0.6, 72), (1.2, 76), (1.8, 79), (2.4, 81), (3.2, 79), (4.2, 76), (4.8, 81), (5.4, 84),
           (6.2, 83), (7.3, 79), (7.9, 83), (8.5, 86), (9.4, 88)]
    for at, n in arp:
        place(buf, piano(midi(n), 3.0, amp=0.16), at)
    st = reverb(buf, 2.6, 0.4)[:int(dur * SR)]
    save(OUT / "music_intro.wav", fade(st, 1.2, 4.5))


def title():
    dur = 7.0
    buf = np.zeros(int(dur * SR))
    place(buf, pad([midi(n) for n in (38, 50, 57, 62, 66, 69)], 6.8, amp=0.10, attack=1.6, release=3.5), 0.0)
    # gentle bell chord right when the title lands (~1.0s)
    for at, n in [(0.95, 74), (1.05, 78), (1.15, 81), (1.25, 86), (2.4, 85), (3.4, 81)]:
        place(buf, piano(midi(n), 3.5, amp=0.13), at)
    st = reverb(buf, 2.8, 0.45)[:int(dur * SR)]
    save(OUT / "music_title.wav", fade(st, 0.9, 3.8))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    intro(); title()
