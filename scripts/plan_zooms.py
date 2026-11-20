"""Turn cursor sightings into zoom segments for a screen tutorial.

A "stay" = cursor resting near one spot (consecutive sightings within R px of the
stay's anchor; no sightings in between means the mouse did not move). Stays that
last >= MIN_STAY become zooms centred on the anchor. A zoom ends when the cursor
leaves the zoomed viewport, a page change/scroll happens, or MAX_HOLD is reached.
Consecutive targets that fit the current viewport are panned to, not re-zoomed.

usage: python3 -I plan_zooms.py track.json zooms.json
"""
import json, sys

d = json.load(open(sys.argv[1]))
DUR = d["duration"]
track = [(t, x, y) for t, x, y, *_ in d["track"]]
cuts = d["cuts"]
W, H = 1920, 1080
R = 110            # px: cursor still "at the same spot"
MIN_STAY = 2.2     # s of resting before we zoom
SCALE = 1.6
MAX_HOLD = 14.0
LEAD = 0.25        # start zooming slightly before the stay begins
GAP = 1.2          # min time at full view between zooms
EXCL = lambda x, y: y < 105 or y > 1005   # macOS menu bar / Chrome tabs+URL bar / dock

def cut_between(a, b):
    return any(not (c1 < a or c0 > b) for c0, c1 in cuts)

# 1) stays
stays = []
cur = None
for t, x, y in track:
    if cur and abs(x - cur["x"]) <= R and abs(y - cur["y"]) <= R:
        cur["last"] = t; cur["pts"].append((x, y))
        continue
    if cur:
        cur["end"] = t           # cursor moved away at t
        stays.append(cur)
    cur = {"start": t, "last": t, "x": x, "y": y, "pts": [(x, y)]}
if cur:
    cur["end"] = DUR; stays.append(cur)

# the stay really starts when the cursor arrives (its last sighting while moving in),
# and ends when it moves away again; trim at the first cut inside the stay
good = []
for s in stays:
    a, b = s["last"], s["end"]
    for c0, c1 in cuts:
        if a < c0 < b:
            b = c0; break
    if b - a >= MIN_STAY and not EXCL(s["x"], s["y"]):
        pts = s["pts"][-4:]   # where it settled: last few sightings of the stay
        mx = round(sum(p[0] for p in pts) / len(pts)); my = round(sum(p[1] for p in pts) / len(pts))
        good.append({"a": round(a, 2), "b": round(b, 2), "x": mx, "y": my})

def viewport(x, y, s=SCALE):
    vw, vh = W / s, H / s
    x0 = min(max(x - vw / 2, 0), W - vw); y0 = min(max(y - vh / 2, 0), H - vh)
    return x0, y0, vw, vh

# 2) zoom segments (merge / pan)
segs = []
for g in good:
    a, b = max(g["a"] - LEAD, 0), min(g["b"], g["a"] + MAX_HOLD)
    if segs:
        p = segs[-1]
        x0, y0, vw, vh = viewport(*p["targets"][-1][1:])
        inside = x0 + 60 < g["x"] < x0 + vw - 60 and y0 + 60 < g["y"] < y0 + vh - 60
        close = a - p["b"] < 2.5 and not cut_between(p["b"], g["a"])
        if close and (b - p["a"]) <= MAX_HOLD * 2:
            # stay zoomed: pan only if the new spot is outside the current view
            if not inside:
                p["targets"].append([round(g["a"], 2), g["x"], g["y"]])
            p["b"] = b
            continue
        if a - p["b"] < GAP:
            a = p["b"] + GAP
            if b - a < 1.5:
                continue
    segs.append({"a": round(a, 2), "b": round(b, 2), "targets": [[round(a, 2), g["x"], g["y"]]]})

zoomed = sum(s["b"] - s["a"] for s in segs)
print(f"stays={len(stays)} usable={len(good)} zoom segments={len(segs)} pans={sum(len(s['targets'])-1 for s in segs)} zoomed {zoomed/DUR*100:.0f}% of {DUR/60:.1f} min", file=sys.stderr)
json.dump({"scale": SCALE, "segments": segs}, open(sys.argv[2], "w"), indent=1)
