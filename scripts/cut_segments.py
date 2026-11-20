#!/usr/bin/env python3
"""Remove time ranges (cuts.json from find_fillers.py) from a video.

Keeps everything outside the cuts and joins the pieces with a 10 ms audio
fade on each side of every join (no clicks). Video is re-encoded once
(H.264 8-bit, CRF 18, 1 s GOP) so the joins are frame-accurate.

Optional --track remaps a cursor_track.json (track_cursor_dense.py format:
{"fps", "duration", "pts": [[frame, x, y, kind], ...]}) onto the new
timeline, so the cursor doesn't need re-tracking after the cut.

usage: python3 -I cut_segments.py <in.mp4> <cuts.json> <out.mp4>
         [--track in_track.json out_track.json]
"""
import argparse, json, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("cuts"); ap.add_argument("out")
ap.add_argument("--track", nargs=2, metavar=("IN", "OUT"))
a = ap.parse_args()

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True).stdout)
cuts = sorted((float(c[0]), float(c[1])) for c in json.load(open(a.cuts))["cuts"])
keep, t = [], 0.0
for c0, c1 in cuts:
    if c0 > t: keep.append((t, c0))
    t = max(t, c1)
if t < dur: keep.append((t, dur))

F = 0.01
parts, labels = [], []
for i, (k0, k1) in enumerate(keep):
    fo = max(k1 - k0 - F, 0)
    parts.append(f"[0:v]trim={k0:.3f}:{k1:.3f},setpts=PTS-STARTPTS[v{i}]")
    parts.append(f"[0:a]atrim={k0:.3f}:{k1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={F},afade=t=out:st={fo:.3f}:d={F}[a{i}]")
    labels.append(f"[v{i}][a{i}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.video, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
       "-g", "30", "-keyint_min", "30", "-sc_threshold", "0", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
       "-movflags", "+faststart", a.out]
subprocess.run(cmd, check=True)

removed = sum(c1 - c0 for c0, c1 in zip([k[1] for k in keep[:-1]], [k[0] for k in keep[1:]]))
print(f"{len(keep) - 1} joins, {removed:.2f}s removed: {dur:.2f}s -> {dur - removed:.2f}s -> {a.out}", file=sys.stderr)

def new_time(t):
    """old timeline -> new timeline, None if t falls inside a cut"""
    shift = 0.0
    for k0, k1 in keep:
        if t < k0: return None
        if t < k1: return t - k0 + shift
        shift += k1 - k0
    return None

if a.track:
    tr = json.load(open(a.track[0])); fps = tr["fps"]; pts = []
    for f, x, y, kind in tr["pts"]:
        nt = new_time(f / fps)
        if nt is not None:
            nf = round(nt * fps)
            if not pts or nf > pts[-1][0]: pts.append([nf, x, y, kind])
    tr["pts"] = pts; tr["duration"] = round(dur - removed, 3)
    json.dump(tr, open(a.track[1], "w"))
    print(f"track: {len(pts)} cursor samples remapped -> {a.track[1]}", file=sys.stderr)
