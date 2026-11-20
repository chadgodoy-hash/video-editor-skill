#!/usr/bin/env python3
"""Forced-align words in a short audio clip with wav2vec2 CTC (precise to ~20 ms).

Whisper's word times drift by up to ±0.5 s, which is too loose for cutting
"umm"s. CTC forced alignment pins every word to the audio. Runs in the
~/.venvs/align venv (transformers on top of the system torch); the model
(facebook/wav2vec2-base-960h, ~380 MB) downloads on first use.

Library use:  from ctc_align import align; align(wav_16k_float32, "so dito um pagpasok")
              -> [(word, start_s, end_s), ...]
CLI:          ~/.venvs/align/bin/python ctc_align.py <clip.wav> "<transcript>"
"""
import os, re, sys
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from transformers.utils import logging as _hf_logging
_hf_logging.set_verbosity_error()

MODEL = "facebook/wav2vec2-base-960h"
_proc = _model = None

def _load():
    global _proc, _model
    if _model is None:
        _proc = Wav2Vec2Processor.from_pretrained(MODEL)
        _model = Wav2Vec2ForCTC.from_pretrained(MODEL).eval()
    return _proc, _model

def align(audio, text, sr=16000):
    proc, model = _load()
    words = [w for w in re.sub(r"[^A-Z' ]", " ", text.upper().replace("-", " ")).split() if w.strip("'")]
    if not words:
        return []
    with torch.inference_mode():
        iv = proc(audio, sampling_rate=sr, return_tensors="pt").input_values
        lp = torch.log_softmax(model(iv).logits[0], -1).numpy()       # T x V
    vocab = proc.tokenizer.get_vocab(); blank = vocab["<pad>"]; sep = vocab["|"]
    toks, owner = [], []                                               # char tokens + which word
    for i, w in enumerate(words):
        if i: toks.append(sep); owner.append(-1)
        for ch in w:
            if ch in vocab: toks.append(vocab[ch]); owner.append(i)
    T, N = lp.shape[0], len(toks)
    # CTC Viterbi over the blank-interleaved sequence
    S = 2 * N + 1
    lab = [blank if s % 2 == 0 else toks[s // 2] for s in range(S)]
    NEG = -1e18
    dp = np.full((T, S), NEG); bp = np.zeros((T, S), np.int32)
    dp[0, 0] = lp[0, blank]; dp[0, 1] = lp[0, lab[1]]
    for t in range(1, T):
        for s in range(S):
            c = [(dp[t - 1, s], s)]
            if s >= 1: c.append((dp[t - 1, s - 1], s - 1))
            if s >= 2 and lab[s] != blank and lab[s] != lab[s - 2]: c.append((dp[t - 1, s - 2], s - 2))
            v, k = max(c); dp[t, s] = v + lp[t, lab[s]]; bp[t, s] = k
    s = S - 1 if dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    path = []
    for t in range(T - 1, -1, -1):
        path.append((t, s)); s = bp[t, s]
    path.reverse()
    hop = len(audio) / sr / T                                          # ~20 ms per frame
    span = {}
    for t, s in path:
        if s % 2 == 1 and owner[s // 2] >= 0:
            i = owner[s // 2]; a, b = span.get(i, (t, t)); span[i] = (min(a, t), max(b, t))
    return [(words[i], span[i][0] * hop, (span[i][1] + 1) * hop) for i in sorted(span)]

if __name__ == "__main__":
    import wave
    w = wave.open(sys.argv[1]); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    for wd, s, e in align(a, sys.argv[2], w.getframerate()):
        print(f"{s:6.2f} {e:6.2f}  {wd}")
