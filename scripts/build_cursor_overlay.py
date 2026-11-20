"""Build a HyperFrames composition for a screen tutorial: footage + a bigger pointer with a
soft yellow glow that follows the creator's real cursor (from track_cursor_dense.py) + music bed.

The overlay draws a larger macOS arrow / pointing hand exactly over the real one (hotspot
on hotspot), so the real cursor is hidden underneath. It holds while the cursor rests,
interpolates between 15 fps samples, and fades out where the tracker lost the cursor
(typing, I-beam over text fields) instead of drifting away from it.

usage: python3 -I build_cursor_overlay.py <track.json> <video src> <duration s> <out.html>
         [--music assets/music/bed.wav] [--music-vol 0.5] [--start 0]
"""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("track"); ap.add_argument("video"); ap.add_argument("duration", type=float); ap.add_argument("out")
ap.add_argument("--music"); ap.add_argument("--music-vol", type=float, default=0.5)
ap.add_argument("--scale", type=float, default=1.9, help="pointer size vs the real cursor")
a = ap.parse_args()

d = json.load(open(a.track))
pts = d["pts"]
F = [p[0] for p in pts]; X = [p[1] for p in pts]; Y = [p[2] for p in pts]; K = [p[3] for p in pts]
DUR = round(a.duration, 2)
music = (f'<audio id="music-bed" class="clip" src="{a.music}" data-start="0" data-duration="{DUR}" '
         f'data-volume="{a.music_vol}" data-track-index="40"></audio>') if a.music else ""

html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #stage {{ position: absolute; inset: 0; overflow: hidden; }}
      #ptr {{ position: absolute; left: 0; top: 0; width: 0; height: 0; opacity: 0; will-change: transform, opacity; }}
      #glow {{ position: absolute; left: -38px; top: -38px; width: 76px; height: 76px; border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 214, 10, 0.55) 0%, rgba(255, 214, 10, 0.32) 42%, rgba(255, 214, 10, 0) 70%); }}
      .cur {{ position: absolute; overflow: visible; filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.45)); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <div id="stage">
        <video id="a-roll" class="clip" src="{a.video}" playsinline data-start="0" data-duration="{DUR}" data-track-index="0" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover" data-has-audio="true"></video>
        <div id="ptr">
          <div id="glow"></div>
          <svg id="arrow" class="cur" viewBox="0 0 14 21" style="left: -{1 * a.scale:.1f}px; top: -{1 * a.scale:.1f}px; width: {14 * a.scale:.1f}px; height: {21 * a.scale:.1f}px">
            <path d="M1,1 L1,16.5 L4.6,13 L7.2,19.2 L9.6,18.2 L7,12.2 L12,12.2 Z" fill="#000" stroke="#fff" stroke-width="1.3" stroke-linejoin="round" />
          </svg>
          <svg id="hand" class="cur" viewBox="0 0 16 23" style="left: -{6.5 * a.scale:.1f}px; top: -{0.6 * a.scale:.1f}px; width: {16 * a.scale:.1f}px; height: {23 * a.scale:.1f}px; opacity: 0">
            <path d="M5.5,2 Q5.5,0.6 6.5,0.6 Q7.5,0.6 7.5,2 L7.5,7.8 Q7.5,6.8 8.5,6.8 Q9.5,6.8 9.5,7.8 L9.5,8.6 Q9.5,7.6 10.5,7.6 Q11.5,7.6 11.5,8.6 L11.5,9.4 Q11.5,8.4 12.5,8.4 Q13.5,8.4 13.5,9.4 L13.5,15 Q13.5,19.5 10.5,21.5 L7,21.5 Q5.6,21.5 4.8,20 L1.6,14.6 Q1,13.4 2.2,13 Q3,12.8 3.7,13.6 L5.5,15.8 Z" fill="#fff" stroke="#000" stroke-width="1" stroke-linejoin="round" />
            <path d="M7.5,9 L7.5,12.5 M9.5,9.5 L9.5,12.5 M11.5,10 L11.5,12.8" stroke="#000" stroke-width="0.8" stroke-linecap="round" />
          </svg>
        </div>
      </div>
      {music}
    </div>
    <script>
      // Dense cursor track (track_cursor_dense.py): frame @ {d["fps"]} fps, hotspot x/y, kind 0 arrow / 1 hand
      const FPS = {d["fps"]};
      const F = {json.dumps(F, separators=(",", ":"))};
      const X = {json.dumps(X, separators=(",", ":"))};
      const Y = {json.dumps(Y, separators=(",", ":"))};
      const K = {json.dumps(K, separators=(",", ":"))};
      const BRIDGE = 3, FADE = 3;   // frames: interpolate across short gaps; fade over 0.2 s
      const ptr = document.getElementById("ptr");
      const arrow = document.getElementById("arrow");
      const hand = document.getElementById("hand");
      const glow = document.getElementById("glow");
      const GLOW_OFF = [[{9 * a.scale / 1.9:.0f}, {17 * a.scale / 1.9:.0f}], [{3 * a.scale / 1.9:.0f}, {21 * a.scale / 1.9:.0f}]];   // glow centre on the pointer body (arrow, hand)
      let lastKind = -1;
      function find(fr) {{   // last index with F[i] <= fr
        let lo = 0, hi = F.length - 1, r = -1;
        while (lo <= hi) {{ const m = (lo + hi) >> 1; if (F[m] <= fr) {{ r = m; lo = m + 1; }} else hi = m - 1; }}
        return r;
      }}
      function place(t) {{
        const fr = t * FPS, i = find(fr), j = i + 1;
        let x = 0, y = 0, k = 0, op = 0;
        if (i >= 0 && j < F.length && F[j] - F[i] <= BRIDGE) {{
          const u = (fr - F[i]) / (F[j] - F[i]);
          x = X[i] + (X[j] - X[i]) * u; y = Y[i] + (Y[j] - Y[i]) * u; k = K[i]; op = 1;
        }} else {{
          if (i >= 0) {{ const o = 1 - Math.max(0, fr - F[i] - 1) / FADE; if (o > op) {{ op = o; x = X[i]; y = Y[i]; k = K[i]; }} }}
          if (j < F.length) {{ const o = 1 - Math.max(0, F[j] - fr - 1) / FADE; if (o > op) {{ op = o; x = X[j]; y = Y[j]; k = K[j]; }} }}
        }}
        op = Math.max(0, Math.min(1, op));
        ptr.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px)";
        ptr.style.opacity = op.toFixed(3);
        if (k !== lastKind) {{ arrow.style.opacity = k ? 0 : 1; hand.style.opacity = k ? 1 : 0; glow.style.transform = "translate(" + GLOW_OFF[k][0] + "px," + GLOW_OFF[k][1] + "px)"; lastKind = k; }}
      }}
      const tl = gsap.timeline({{ paused: true }});
      const proxy = {{ t: 0 }};
      tl.fromTo(proxy, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", immediateRender: false, onUpdate: () => place(proxy.t) }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(a.out, "w").write(html)
print(f"{len(F)} cursor samples, duration {DUR}s -> {a.out}")
