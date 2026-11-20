"""Cursor tracker v2: motion candidates + cursor-template confirmation.

Streams full-res gray frames at FPS. Half-res frame diff finds small moving blobs
(outside the webcam, which moves constantly). Each candidate is confirmed by
normalized cross-correlation with the creator's macOS arrow (tmpl_arrow.npy, tip at
(+3,+3)); score >= NCC_T means "this is the cursor". Big diffs = page change/scroll.

usage: python3 -I track_cursor.py <video> assets/cursor/macos_arrow.npy <out.json>
"""
import json, subprocess, sys
import numpy as np
from scipy import ndimage
from scipy.signal import fftconvolve

VID, TPL, OUT = sys.argv[1:4]
import os
W, H, FPS = 1920, 1080, int(os.environ.get("TRACK_FPS", 6))   # 15 for a smooth cursor glow
DIFF_T, BIG_FRAC = 28, 0.06
CUR_MIN, CUR_MAX = 6, 900        # half-res blob area
GRID, CAM_FRAC, WIN = 16, 0.35, 30
NCC_T, SEARCH = 0.76, 70          # accept score, search radius (full-res px)

T = np.load(TPL).astype(np.float64)
Tz = T - T.mean(); TN = np.sqrt((Tz ** 2).sum()); K = np.ones_like(T)

def ncc_best(img, cx, cy):
    x0, y0 = int(max(cx - SEARCH, 0)), int(max(cy - SEARCH, 0))
    x1, y1 = int(min(cx + SEARCH, W)), int(min(cy + SEARCH, H))
    w = img[y0:y1, x0:x1]
    if w.shape[0] <= T.shape[0] or w.shape[1] <= T.shape[1]:
        return 0, None
    n = T.size
    s = fftconvolve(w, K, 'valid'); s2 = fftconvolve(w * w, K, 'valid')
    var = np.maximum(s2 - s * s / n, 0)
    r = fftconvolve(w, Tz[::-1, ::-1], 'valid') / (np.sqrt(var) * TN + 1e-9)
    r[var / n < 150] = 0
    iy, ix = np.unravel_index(r.argmax(), r.shape)
    return float(r.max()), (x0 + ix + 3, y0 + iy + 3)

cmd = ["/opt/homebrew/bin/ffmpeg", "-v", "error", "-i", VID, "-vf", f"fps={FPS},format=gray", "-f", "rawvideo", "-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
fsz = W * H
prev = None; i = 0
recs = []   # (t, frac, cands[(cy,cx) full-res], cellmask, img-needed later?) -> confirm inline
cellmasks = []
pending = []  # store candidates and confirm after webcam mask known? confirm inline, filter webcam later
while True:
    buf = p.stdout.read(fsz)
    if len(buf) < fsz:
        break
    full = np.frombuffer(buf, np.uint8).reshape(H, W)
    f = full[::2, ::2].astype(np.int16)
    t = i / FPS
    if prev is not None:
        m = np.abs(f - prev) > DIFF_T
        frac = float(m.mean())
        hh, ww = (540 // GRID) * GRID, (960 // GRID) * GRID
        cm = m[:hh, :ww].reshape(hh // GRID, GRID, ww // GRID, GRID).any(axis=(1, 3))
        cellmasks.append((t, frac, cm))
        hits = []
        if 0 < frac < BIG_FRAC:
            lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=2))
            if n:
                idx = np.arange(1, n + 1)
                areas = ndimage.sum(m, lab, idx); coms = ndimage.center_of_mass(m, lab, idx)
                cands = [(cy * 2, cx * 2) for a, (cy, cx) in zip(areas, coms) if CUR_MIN <= a <= CUR_MAX]
                img = None
                for cy, cx in cands[:6]:
                    if img is None:
                        img = full.astype(np.float64)
                    sc, pos = ncc_best(img, cx, cy)
                    if sc >= NCC_T:
                        hits.append((sc, pos))
        recs.append((t, frac, hits))
    prev = f; i += 1
p.wait()
dur = i / FPS

# webcam mask per window (cells moving most of the time) — drop hits inside it
cam = {}
for w0 in range(0, int(dur) + WIN, WIN):
    sel = [cm for t, fr, cm in cellmasks if w0 <= t < w0 + WIN and fr < BIG_FRAC]
    if sel:
        cam[w0] = ndimage.binary_dilation(np.mean(sel, axis=0) > CAM_FRAC, iterations=2)
def in_cam(t, x, y):
    mk = cam.get(int(t // WIN) * WIN)
    if mk is None: return False
    gy = min(int(y / 2 // GRID), mk.shape[0] - 1); gx = min(int(x / 2 // GRID), mk.shape[1] - 1)
    return bool(mk[gy, gx])

track, cuts = [], []
for t, fr, hits in recs:
    if fr >= BIG_FRAC:
        cuts.append(round(t, 2)); continue
    hits = [h for h in hits if not in_cam(t, *h[1])]
    if hits:
        sc, (x, y) = max(hits)
        track.append((round(t, 2), int(x), int(y), round(sc, 2)))
ev = []
for t in cuts:
    if not ev or t - ev[-1][1] > 0.6: ev.append([t, t])
    else: ev[-1][1] = t
json.dump({"duration": dur, "fps": FPS, "track": track, "cuts": ev}, open(OUT, "w"))
print(f"dur={dur:.1f}s confirmed cursor points={len(track)} cut events={len(ev)}", file=sys.stderr)
