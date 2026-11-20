"""Dense cursor track for a cursor overlay (bigger pointer + glow) in screen tutorials.

Unlike track_cursor.py (which only reports the cursor when it moves), this confirms the
arrow on EVERY frame: a still check at the last known position plus motion candidates,
both verified by NCC against the creator's macOS arrow. Frames where the arrow can't be found
(hidden while typing, or a hand / I-beam cursor over links and text fields) are absent,
so the overlay can fade out instead of drifting away from the real cursor.

Pass 1 (3 fps, half-res) finds the webcam bubble (cells moving most of the time).
Pass 2 (FPS, full-res gray) tracks.

Templates (assets/cursor/): macos_arrow.npy (tip at +3,+3) and macos_hand.npy (pointing
hand over links, fingertip at +5,+2). The I-beam is not tracked: it is too thin and matches
letters like "I"/"l", so the overlay just fades while the creator is in a text field.

usage: TRACK_FPS=15 python3 -I track_cursor_dense.py <video> <out.json>
out: {"fps", "duration", "pts": [[frame, x, y, kind], ...]}  (x, y = hotspot, 1920x1080; kind 0 arrow, 1 hand)
"""
import json, os, subprocess, sys
import numpy as np
from scipy import ndimage
from scipy.signal import fftconvolve

VID, OUT = sys.argv[1:3]
CUR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "cursor")
W, H = 1920, 1080
FPS = int(os.environ.get("TRACK_FPS", 15))
FF = "/opt/homebrew/bin/ffmpeg"
DIFF_T, BIG_FRAC = 28, 0.06
CUR_MIN, CUR_MAX = 6, 900          # half-res motion blob area
GRID, CAM_FRAC, WIN = 16, 0.35, 30
NCC_T = (0.80, 0.80)                # masked-NCC accept score (arrow, hand); static UI icons score ~0.7
SEARCH, STILL = 70, 14             # motion search radius / still-check radius (px)

# Masked NCC: only the cursor's own pixels (fill + 1 px outline) count, so the match
# survives any background (white page, dark sidebar, hover-highlighted rows).
TPLS = []   # (template, flipped masked zero-mean, norm, flipped mask, hotspot offset)
for name, off in (("macos_arrow.npy", (3, 3)), ("macos_hand.npy", (5, 2))):
    T = np.load(os.path.join(CUR_DIR, name)).astype(np.float64)
    bg = np.median(np.concatenate([T[0], T[-1], T[:, 0], T[:, -1]]))
    M = ndimage.binary_dilation(np.abs(T - bg) > 40, iterations=1)
    Tm = (T - T[M].mean()) * M
    TPLS.append((T, Tm[::-1, ::-1], np.sqrt((Tm ** 2).sum()), M.astype(np.float64)[::-1, ::-1], off))

def ncc_best(img, hx, hy, rad):
    """Best (score, hotspot, kind) over all templates, hotspot within rad of (hx, hy)."""
    best = (0.0, None, -1)
    for kind, (T, TF, TN, K, (ox, oy)) in enumerate(TPLS):
        x0, y0 = int(max(hx - ox - rad, 0)), int(max(hy - oy - rad, 0))
        x1, y1 = int(min(hx - ox + rad + T.shape[1], W)), int(min(hy - oy + rad + T.shape[0], H))
        w = img[y0:y1, x0:x1]
        if w.shape[0] <= T.shape[0] or w.shape[1] <= T.shape[1]:
            continue
        n = K.sum()
        s = fftconvolve(w, K, 'valid'); s2 = fftconvolve(w * w, K, 'valid')
        var = np.maximum(s2 - s * s / n, 0)
        r = fftconvolve(w, TF, 'valid') / (np.sqrt(var) * TN + 1e-9)
        r[var / n < 150] = 0
        iy, ix = np.unravel_index(r.argmax(), r.shape)
        if r.max() >= NCC_T[kind] and r.max() - NCC_T[kind] > best[0] - (NCC_T[best[2]] if best[2] >= 0 else 0):
            best = (float(r.max()), (x0 + ix + ox, y0 + iy + oy), kind)
    return best

def frames(vf, w, h):
    p = subprocess.Popen([FF, "-v", "error", "-i", VID, "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    sz = w * h
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w)
    p.wait()

# pass 1: webcam mask per 30 s window
cells = {}
prev = None
for i, f in enumerate(frames("fps=3,scale=960:540,format=gray", 960, 540)):
    f = f.astype(np.int16)
    if prev is not None:
        m = np.abs(f - prev) > DIFF_T
        if m.mean() < BIG_FRAC:
            hh, ww = (540 // GRID) * GRID, (960 // GRID) * GRID
            cm = m[:hh, :ww].reshape(hh // GRID, GRID, ww // GRID, GRID).any(axis=(1, 3))
            cells.setdefault(int(i / 3 // WIN) * WIN, []).append(cm)
    prev = f
cam = {k: ndimage.binary_dilation(np.mean(v, axis=0) > CAM_FRAC, iterations=2) for k, v in cells.items()}

def in_cam(t, x, y):
    mk = cam.get(int(t // WIN) * WIN)
    if mk is None:
        return False
    return bool(mk[min(int(y / 2 // GRID), mk.shape[0] - 1), min(int(x / 2 // GRID), mk.shape[1] - 1)])

# pass 2: dense track
pts = []
last = None
prev = None
n = 0
for n, full in enumerate(frames(f"fps={FPS},format=gray", W, H)):
    t = n / FPS
    img = full.astype(np.float64)
    half = full[::2, ::2].astype(np.int16)
    best = None
    if last is not None:
        sc, pos, kd = ncc_best(img, last[0], last[1], STILL)
        if kd >= 0:
            best = (sc, pos, kd)
    if prev is not None:   # always look at motion: a real moving cursor beats a still match
        m = np.abs(half - prev) > DIFF_T
        frac = float(m.mean())
        if 0 < frac < BIG_FRAC:
            lab, k = ndimage.label(ndimage.binary_dilation(m, iterations=2))
            if k:
                idx = np.arange(1, k + 1)
                areas = ndimage.sum(m, lab, idx); coms = ndimage.center_of_mass(m, lab, idx)
                cands = [(cy * 2, cx * 2) for a, (cy, cx) in zip(areas, coms) if CUR_MIN <= a <= CUR_MAX]
                if last is not None:   # nearest to the last position first
                    cands.sort(key=lambda c: (c[1] - last[0]) ** 2 + (c[0] - last[1]) ** 2)
                for cy, cx in cands[:6]:
                    sc, pos, kd = ncc_best(img, cx, cy, SEARCH)
                    if kd >= 0 and not in_cam(t, *pos):
                        moved = best is None or abs(pos[0] - best[1][0]) + abs(pos[1] - best[1][1]) > 6
                        if best is None or moved or sc > best[0]:
                            best = (sc, pos, kd)
                        break
    if best and not in_cam(t, *best[1]):
        last = best[1]
        pts.append([n, int(last[0]), int(last[1]), best[2]])
    else:
        last = None if best is None else last
    prev = half
dur = (n + 1) / FPS
json.dump({"fps": FPS, "duration": dur, "pts": pts}, open(OUT, "w"), separators=(",", ":"))
print(f"dur={dur:.1f}s frames={n + 1} cursor present in {len(pts)} ({len(pts) / (n + 1) * 100:.0f}%)", file=sys.stderr)
