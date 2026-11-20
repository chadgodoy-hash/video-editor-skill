#!/usr/bin/env python3
"""Turn a downloaded sound-effect pack into clean, leveled clips for a HyperFrames project.

Usage:
  python3 sfx_kit.py <out_dir> <pack file or folder> [<pack file or folder> ...]

What it does:
  1. Every audio file in the pack(s) is split on silence (-45 dB, 0.25 s gaps) into
     individual clips: <name>-1.wav, <name>-2.wav, ...  (single-sound files stay as one clip)
  2. Adds a 10 ms fade-in and 60 ms fade-out so cuts never click.
  3. Loudness-normalizes every clip to -18 LUFS / -3 dBTP at 48 kHz.
  4. Prints a table: clip, duration, peak dB, where the loudest moment sits.
     Short + loud-at-start = pop/hit/tick. Long + late peak = riser/big whoosh.

Claude cannot listen to audio — this table is how clips are characterized.
Requires ffmpeg/ffprobe at /opt/homebrew/bin.
"""
import os
import re
import subprocess
import sys

FF = "/opt/homebrew/bin/ffmpeg"
FP = "/opt/homebrew/bin/ffprobe"
AUDIO_EXT = (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".aif", ".aiff")


def duration(path):
    out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def sounds(path):
    """Return (start, end) spans of non-silent audio."""
    total = duration(path)
    log = subprocess.run([FF, "-hide_banner", "-i", path, "-af", "silencedetect=noise=-45dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    spans, cur = [], 0.0
    for s, e in zip(starts, ends + [total]):
        if s - cur > 0.04:
            spans.append((max(0.0, cur - 0.02), min(total, s + 0.05)))
        cur = e
    if total - cur > 0.04:
        spans.append((max(0.0, cur - 0.02), total))
    return spans or [(0.0, total)]


def measure(path):
    d = duration(path)
    log = subprocess.run([FF, "-hide_banner", "-i", path, "-af",
                          "astats=metadata=1:reset=1:measure_overall=none:measure_perchannel=RMS_level,"
                          "ametadata=print:key=lavfi.astats.1.RMS_level", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    vals = [float(v) for v in re.findall(r"RMS_level=(-?[\d.]+)", log)]
    plog = subprocess.run([FF, "-hide_banner", "-i", path, "-af",
                           "astats=measure_overall=Peak_level:measure_perchannel=none", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    peak = re.findall(r"Peak level dB: (\S+)", plog)
    loudest = (max(range(len(vals)), key=lambda k: vals[k]) / len(vals) * d) if vals else 0
    return d, (peak[-1] if peak else "?"), loudest


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for p in sys.argv[2:]:
        if os.path.isdir(p):
            files += [os.path.join(r, f) for r, _, fs in os.walk(p) for f in sorted(fs) if f.lower().endswith(AUDIO_EXT)]
        else:
            files.append(p)
    print(f"{'clip':<34} {'dur':>6} {'peak dB':>8} {'loudest at':>10}")
    for f in files:
        base = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(f))[0].lower()).strip("-")[:24]
        spans = sounds(f)
        for i, (a, b) in enumerate(spans, 1):
            name = f"{base}-{i}.wav" if len(spans) > 1 else f"{base}.wav"
            out = os.path.join(out_dir, name)
            d = b - a
            fade = (f"afade=t=in:d=0.01,afade=t=out:st={max(0, d - 0.06):.3f}:d=0.06,"
                    "loudnorm=I=-18:TP=-3:LRA=7,aformat=sample_rates=48000")
            subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", f, "-af", fade, "-ar", "48000", out],
                           check=True)
            dur, peak, loud = measure(out)
            print(f"{name:<34} {dur:>5.2f}s {peak:>8} {loud:>9.2f}s")


if __name__ == "__main__":
    main()
