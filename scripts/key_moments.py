#!/usr/bin/env python3
"""Print word-level timings from a whisper.cpp JSON transcript (-ojf output).

Usage:
  python3 key_moments.py transcript.json                 # every segment
  python3 key_moments.py transcript.json 29-50 120-150   # only segments starting in these second ranges

Each line: --- <segment start>  word@seconds|word@seconds|...
Use it to sync overlays, caption underlines and SFX to the exact spoken word.
"""
import json
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1]))
    ranges = []
    for r in sys.argv[2:]:
        a, b = r.split("-")
        ranges.append((float(a), float(b)))
    for seg in data["transcription"]:
        start = seg["offsets"]["from"] / 1000
        if ranges and not any(a <= start < b for a, b in ranges):
            continue
        words = [
            f'{t["text"]}@{t["offsets"]["from"] / 1000:.2f}'
            for t in seg["tokens"]
            if not t["text"].startswith("[_")
        ]
        print(f"--- {start:.2f}", "|".join(words))


if __name__ == "__main__":
    main()
