#!/usr/bin/env python3
"""Build small-subtitle cues (SUB_CUES) from a whisper.cpp JSON transcript (-ojf).

Usage:
  python3 build_subtitles.py transcript.json [--fixes fixes.json] [--end 145.6] [--max 44] > cues.json

- Merges whisper sub-word tokens into words (a token with no leading space joins the previous word).
- Breaks a cue at --max characters, at sentence ends, after a comma once the line is > 22 chars,
  or at a pause > 0.6 s.
- Each cue stays on screen until the next one starts, at least 1.0 s, and never past --end
  (the start of the end card / footage end).
- Flags cues whose spoken span is < 0.5 s (Whisper squashed the timing) on stderr — re-time those by hand.

fixes.json (optional): {"wrong text": "right text", ...} — applied to whole words or phrases
inside each cue, e.g. {"Kraming": "Maraming", "ginagawa niya": "ginagawa nyo"}.

Output: JSON array [{"t": text, "s": start, "e": end}, ...] — paste into SUB_CUES in index.html
(see example-composition.html). Review the printed cue list before using it.
"""
import argparse
import json
import re
import sys


def words_from(transcript):
    words = []
    for seg in transcript["transcription"]:
        for tok in seg["tokens"]:
            tx = tok["text"]
            if tx.startswith("[_") or not tx.strip():
                continue
            s, e = tok["offsets"]["from"] / 1000, tok["offsets"]["to"] / 1000
            if tx.startswith(" ") or not words:
                words.append([tx.strip(), s, e])
            else:
                words[-1][0] += tx
                words[-1][2] = e
    return words


def chunk(words, max_chars):
    cues, cur = [], []
    for w in words:
        if cur:
            text = " ".join(x[0] for x in cur)
            gap = w[1] - cur[-1][2]
            if (len(text) + 1 + len(w[0]) > max_chars or gap > 0.6
                    or re.search(r"[.!?]$", cur[-1][0])
                    or (cur[-1][0].endswith(",") and len(text) > 22)):
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)
    return [[" ".join(x[0] for x in c), c[0][1], c[-1][2]] for c in cues]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--fixes")
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--max", type=int, default=44)
    a = ap.parse_args()

    cues = chunk(words_from(json.load(open(a.transcript))), a.max)
    fixes = json.load(open(a.fixes)) if a.fixes else {}
    end_cap = a.end if a.end is not None else cues[-1][2] + 1

    out = []
    for i, (t, s, e) in enumerate(cues):
        for wrong, right in fixes.items():
            t = t.replace(wrong, right)
        if e - s < 0.5:
            print(f"!! squashed timing ({e - s:.2f}s) at {s:.2f}: {t}", file=sys.stderr)
        nxt = cues[i + 1][1] if i + 1 < len(cues) else end_cap
        shown = min(nxt, max(e + 0.6, s + 1.0), end_cap)
        if s < end_cap:
            out.append({"t": t, "s": round(s, 2), "e": round(shown, 2)})
    for c in out:
        print(f"{c['s']:7.2f} {c['e']:7.2f}  {c['t']}", file=sys.stderr)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
