#!/usr/bin/env python3
"""Find the boundaries between sounds in a back-to-back SFX compilation.

Usage:
  python3 split_compilation.py <compilation audio> [expected_count]

Silence gaps alone miss sounds that butt straight into each other, so this
combines two signals:
  1. silence gaps (< -40 dB for >= 0.12 s)
  2. spectral novelty — a sharp change in timbre between the 0.35 s before and
     after each point (cosine distance of log-band spectra), with an energy jump.

Prints JSON: [{"start": s, "end": e}, ...] to stdout. Pass expected_count (e.g. 60
for "Top 60 Sound Effects") to tune the novelty threshold toward that number.
Requires numpy + ffmpeg.
"""
import json
import subprocess
import sys

import numpy as np

FF = "/opt/homebrew/bin/ffmpeg"
SR = 22050
HOP = 441          # 20 ms
WIN = 1024


def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def features(x):
    n = 1 + (len(x) - WIN) // HOP
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    frames = x[idx] * np.hanning(WIN)[None, :]
    mag = np.abs(np.fft.rfft(frames, axis=1))
    # 32 log-spaced bands 40 Hz – 10 kHz
    freqs = np.fft.rfftfreq(WIN, 1 / SR)
    edges = np.geomspace(40, 10000, 33)
    bands = np.stack([mag[:, (freqs >= lo) & (freqs < hi)].sum(axis=1) for lo, hi in zip(edges[:-1], edges[1:])], axis=1)
    logb = np.log1p(bands * 10)
    rms_db = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)
    return logb, rms_db


def novelty(logb, rms_db, half=17):  # 17 frames = 0.34 s each side
    n = len(logb)
    nov = np.zeros(n)
    for i in range(half, n - half):
        a = logb[i - half:i].mean(axis=0)
        b = logb[i:i + half].mean(axis=0)
        cos = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
        jump = max(0.0, rms_db[i:i + 5].max() - rms_db[i - 5:i].mean())   # attack right after the point
        nov[i] = (1 - cos) * (1 + jump / 12)
    return nov


def peaks(sig, thr, min_gap):
    out = []
    for i in range(1, len(sig) - 1):
        if sig[i] >= thr and sig[i] >= sig[i - 1] and sig[i] >= sig[i + 1]:
            if out and i - out[-1] < min_gap:
                if sig[i] > sig[out[-1]]:
                    out[-1] = i
            else:
                out.append(i)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    x = load(sys.argv[1])
    want = int(sys.argv[2]) if len(sys.argv) > 2 else None
    logb, rms_db = features(x)
    n = len(rms_db)
    t = lambda i: i * HOP / SR

    silent = rms_db < -40
    # silence runs >= 0.12 s
    cuts = set()
    i = 0
    while i < n:
        if silent[i]:
            j = i
            while j < n and silent[j]:
                j += 1
            if j - i >= 6:
                cuts.add(i)
                cuts.add(j)
            i = j
        else:
            i += 1

    nov = novelty(logb, rms_db)
    min_gap = 30  # 0.6 s between boundaries
    thr = 0.12
    if want:
        lo, hi = 0.01, 1.0
        for _ in range(30):
            thr = (lo + hi) / 2
            count = len(segments(cuts, peaks(nov, thr, min_gap), silent, n))
            if count > want:
                lo = thr
            else:
                hi = thr
    segs = segments(cuts, peaks(nov, thr, min_gap), silent, n)
    print(json.dumps([{"start": round(t(a), 3), "end": round(t(b), 3)} for a, b in segs]))
    print(f"{len(segs)} sounds (novelty threshold {thr:.3f})", file=sys.stderr)


def segments(cuts, nov_peaks, silent, n):
    bounds = sorted(set(cuts) | set(nov_peaks) | {0, n})
    segs = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        # trim silence inside the span
        while a < b and silent[a]:
            a += 1
        while b > a and silent[b - 1]:
            b -= 1
        if b - a >= 8:  # >= 0.16 s of sound
            segs.append((a, b))
    return segs


if __name__ == "__main__":
    main()
