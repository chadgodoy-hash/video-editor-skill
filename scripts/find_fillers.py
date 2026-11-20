#!/usr/bin/env python3
"""Find "umm / ahh / ehh" fillers and plan tight cuts around them.

Whisper drops most fillers. A disfluency prompt brings them back, but its
timestamps are too loose to cut on, and it also invents a few. So this script:

  1. transcribes word by word with a filler-friendly prompt (or reads a saved
     --words JSON from a previous run),
  2. collects candidates: filler tokens + voiced sounds in pauses between words,
  3. confirms each one by re-transcribing a ~4 s window around it (a candidate
     counts only if a filler word shows up there),
  4. forced-aligns that window (ctc_align.py, ~20 ms accurate) and cuts from the
     word before the filler to the word after it, removing the filler and its
     hesitation pause but keeping a natural pause (default 0.25 s).

Output: cuts.json = {"source": ..., "cuts": [[start, end, label], ...], "review": [...]}.
Every cut is printed for review; `review` lists candidates that were skipped
and why. Apply with cut_segments.py.

usage: ~/.venvs/align/bin/python -I find_fillers.py <video or 16 kHz wav> <out cuts.json>
         [--words fill.json] [--keep 0.25] [--model PATH]
"""
import argparse, json, os, re, subprocess, sys, tempfile, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("out")
ap.add_argument("--words", help="whisper -ojf JSON made with -ml 1 -sow (skips step 1)")
ap.add_argument("--keep", type=float, default=0.25, help="pause left where a filler was (s)")
ap.add_argument("--model", default=os.path.expanduser("~/whisper-models/ggml-large-v3-turbo-q5_0.bin"))
a = ap.parse_args()

PROMPT = "Umm, so, uh, ahh, ito, ehm, hmm, uhm... ahh, yung, umm, ano."
FILLER = re.compile(r"^(u+h*m+|u+m+|u+h+|a+h+m*|a+m+|e+h*m*|h+m+|m+h*m+|er+m*)[.,!?…]*$", re.I)
tmp = tempfile.mkdtemp(prefix="fillers-")

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

# --- audio -----------------------------------------------------------------
wav = os.path.join(tmp, "audio.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-vn", "-ac", "1", "-ar", "16000", wav])
w = wave.open(wav); SR = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
HOP = SR // 100                                            # 10 ms frames
n = len(x) // HOP
db = 20 * np.log10(np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1)) + 1e-9)
floor, speech = np.percentile(db, 10), np.percentile(db, 70)
THR = floor + 0.40 * (speech - floor)                      # "something is sounding"
loud = db > THR

def voicing(t0, t1):
    """longest run (frames) of pitched sound, 75-350 Hz autocorrelation > 0.6"""
    best = runl = 0
    for t in np.arange(max(t0, 0), t1 - 0.03, 0.01):
        s = x[int(t * SR):int((t + 0.03) * SR)]; s = s - s.mean(); e = (s * s).sum()
        r = 0 if e < 1e-5 else (np.correlate(s, s, "full")[len(s) - 1:] / e)[SR // 350:SR // 75].max()
        runl = runl + 1 if r > 0.6 else 0; best = max(best, runl)
    return best * 10

# --- 1. words --------------------------------------------------------------
words_json = a.words
if not words_json:
    base = os.path.join(tmp, "fill")
    run(["whisper-cli", "-m", a.model, "-f", wav, "-l", "en", "--prompt", PROMPT, "--carry-initial-prompt",
         "-ml", "1", "-sow", "--dtw", "large.v3.turbo", "-ojf", "-of", base])
    words_json = base + ".json"
ws = [(s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip())
      for s in json.load(open(words_json))["transcription"] if s["text"].strip()]

# --- 2. candidates ---------------------------------------------------------
cands = []
for i, (t0, t1, t) in enumerate(ws):
    if FILLER.match(t):
        cands.append((t0, t1, t))
for (p0, p1, pt), (q0, q1, qt) in zip(ws, ws[1:]):
    if FILLER.match(pt) or FILLER.match(qt) or q0 - p1 < 0.35:
        continue
    seg = loud[int((p1 + 0.05) * 100):int((q0 - 0.05) * 100)]
    longest = max((len(r) for r in "".join("1" if v else "0" for v in seg).split("0")), default=0)
    if voicing(p1 + 0.05, q0 - 0.05) >= 120 or (q0 - p1 >= 0.8 and longest >= 15):
        cands.append((p1, q0, "(gap)"))                   # a hum hiding in a pause
cands.sort()

# --- 3 + 4. confirm by re-listening, then align and plan the cut -----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ctc_align import align

def listen(c0, c1):
    """re-transcribe a short window; return (text, window start)"""
    snip = os.path.join(tmp, "snip.wav")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c0:.2f}", "-t", f"{c1 - c0:.2f}", "-i", wav, snip])
    txt = run(["whisper-cli", "-m", a.model, "-f", snip, "-l", "en", "--prompt", "Umm, uh, ahh, ehm, hmm.", "-nt"]).stdout
    return " ".join(txt.split())

cuts, review = [], []
for t0, t1, label in cands:
    # Whisper hears differently depending on the window, so listen twice
    for w0, w1 in ((max(t0 - 2.0, 0), t1 + 1.6), (max(t0 - 1.2, 0), t1 + 2.6)):
        txt = listen(w0, w1)
        if not any(FILLER.match(tk) for tk in re.findall(r"[\w']+", txt)):
            continue
        al = align(x[int(w0 * SR):int(w1 * SR)], txt)
        al = [(wd, w0 + s0, w0 + s1) for wd, s0, s1 in al]
        # the filler nearest the candidate, with a real word on both sides
        idx = [i for i, (wd, _, _) in enumerate(al) if FILLER.match(wd)]
        idx = [i for i in idx if 0 < i < len(al) - 1 and al[i - 1][2] < t1 + 0.8 and al[i + 1][1] > t0 - 0.8]  # its gap overlaps the candidate
        if idx:
            break
    else:
        idx = []
    if not idx:
        review.append({"at": round(t0, 2), "label": label, "skip": "no filler heard (or no word on both sides)", "heard": txt}); continue
    i = min(idx, key=lambda i: abs((al[i][1] + al[i][2]) / 2 - (t0 + t1) / 2))
    # several fillers in a row ("um, ah,") -> take the whole run
    j = i
    while j + 1 < len(al) - 1 and FILLER.match(al[j + 1][0]): j += 1
    while i - 1 > 0 and FILLER.match(al[i - 1][0]): i -= 1
    prev, nxt = al[i - 1], al[j + 1]
    gap0, gap1 = prev[2] + 0.04, nxt[1] - 0.04               # 40 ms guard on each word
    if gap1 - gap0 > 3.0:
        review.append({"at": round(t0, 2), "label": label, "skip": f"gap {gap1 - gap0:.1f}s - too long, check by hand", "heard": txt}); continue
    # the pause we keep must be silence: walk in from each word while frames are quiet
    def quiet_run(t, step):
        k = 0
        while k < a.keep * 50 and not loud[int(round(t * 100)) + step * k]: k += 1
        return k / 100
    kl, kr = quiet_run(gap0, 1), quiet_run(gap1 - 0.01, -1)
    c0, c1 = gap0 + kl, gap1 - kr
    if c1 - c0 < 0.15:
        review.append({"at": round(t0, 2), "label": label, "skip": "cut too small", "heard": txt}); continue
    cuts.append([round(c0, 2), round(c1, 2), f"{prev[0].lower()} [{' '.join(w[0].lower() for w in al[i:j + 1])}] {nxt[0].lower()}  | {txt}"])

# merge overlapping cuts
cuts.sort(); merged = []
for c in cuts:
    if merged and c[0] <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], c[1])
    else: merged.append(c)

json.dump({"source": os.path.abspath(a.media), "keep": a.keep, "cuts": merged, "review": review},
          open(a.out, "w"), indent=1, ensure_ascii=False)
total = sum(c[1] - c[0] for c in merged)
for c in merged: print(f"CUT  {c[0]:8.2f}-{c[1]:8.2f} ({c[1] - c[0]:.2f}s)  {c[2]}", file=sys.stderr)
for r in review: print(f"skip {r['at']:8.2f}  {r['label']}: {r['skip']}  [{r['heard']}]", file=sys.stderr)
print(f"{len(merged)} cuts, {total:.1f}s removed -> {a.out}", file=sys.stderr)
