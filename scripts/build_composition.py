"""Per-video composition generator (first used on "Hard lessons I've learned as a VA", 2026-10-18).

Workflow:
  1. Copy this file + ../templates/lesson-video-template.html (as template.html) + your cues.json
     into one scratch folder.
  2. Edit the data blocks for the new video: CHAPTERS, CAPS (main-point captions), SLAMS (numbered
     lesson cards), the camera moves (punch()/snap() calls — gaps are auto-filled with slow
     push/pull), PANELS (in/out times for whooshes) and the SFX list. Edit the template's
     per-video panels (HTML + their JS blocks) to match the new content.
  3. python3 build_composition.py <hf-project>/index.html
     -> fills __AUDIO__, __CHAPTERS__, __CAPTIONS__, __SLAMS__, __JS__, __CAM__, __CUES__, __HIDE__,
        auto-assigns non-overlapping audio tracks, copies used library clips into assets/sfx/.
Respect the SFX rules in SKILL.md: no banned clips (catalog.json "banned": true), upbeat sounds only.
"""
import json, os, shutil, sys

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
LIB = os.environ.get("SFX_LIB", os.path.expanduser("~/sfx-library"))  # your leveled SFX library folder
ROOT_END = 583.8
SUB_END = 579.6

# ---------------- chapters ----------------
CHAPTERS = [
    ("00", "INTRO", 5.0, 38.7),
    ("01", "LESSON 1 · COMMUNICATION", 38.9, 118.5),
    ("02", "LESSON 2 · EXPERIENCE &gt; DEGREE", 118.7, 170.7),
    ("03", "LESSON 3 · ALWAYS UPSKILL", 170.9, 241.7),
    ("04", "LESSON 4 · CHOOSE YOUR CIRCLE", 241.9, 290.8),
    ("05", "LESSON 5 · LOVE THE JOB, NOT THE COMPANY", 291.0, 354.8),
    ("06", "LESSON 6 · BACKUP PLAN", 355.0, 469.4),
    ("07", "LESSON 7 · SAVE &amp; INVEST", 469.6, 556.9),
    ("&#10003;", "RECAP", 557.0, 579.4),
]

# ---------------- main-point captions: (id, start, end, underline_at, html) ----------------
CAPS = [
    ("c12y", 26.0, 30.4, 28.55, 'Kasi solid naman talaga, <b>12 years<i class="ul"></i></b>.'),
    ("ccomm", 90.3, 92.8, 90.94, 'Dapat marunong ka <b>makipag-communicate<i class="ul"></i></b>.'),
    ("cexp", 164.7, 168.6, 165.15, '<b>Experience<i class="ul"></i></b> speaks louder than your degree.'),
    ("ctamad", 233.7, 239.6, 236.08, 'If ikaw yung tao na <b>tamad matuto<i class="ul"></i></b>, hindi talaga ito para sa\'yo.'),
    ("csupport", 252.6, 256.9, 254.95, 'Surround yourself ng mga taong <b>susuporta<i class="ul"></i></b> sa\'yo.'),
    ("creplace", 320.6, 324.3, 322.23, 'You\'re going to be <b>replaceable<i class="ul"></i></b>.'),
    ("ccompany", 335.4, 342.8, 341.88, 'Love your job, but don\'t fall in love with your <b>company<i class="ul"></i></b>.'),
    ("cjustva", 397.1, 404.4, 403.06, 'A VA job can start a life, but don\'t end it being <b>just a VA<i class="ul"></i></b>.'),
    ("ccash", 409.8, 414.6, 413.6, 'If you\'re already a VA, start your own <b>business cash flow<i class="ul"></i></b>.'),
    ("cwalang", 480.1, 482.4, 480.22, '<b>Walang<i class="ul"></i></b> makakaligtas dito.'),
    ("crainy", 515.0, 518.2, 515.36, 'Para during <b>rainy days<i class="ul"></i></b>, may pagkukunan ka.'),
    ("cfund", 548.3, 551.0, 549.26, 'Always prepare your <b>emergency fund<i class="ul"></i></b>.'),
]

# ---------------- lesson slams: (n, start, end, title_html, extra_html) ----------------
SLAMS = [
    (1, 39.0, 51.6, 'Communication is <em>everything</em>',
     '<div class="extra"><span class="very" id="v1">VERY</span><span class="very" id="v2">VERY</span><span class="very" id="v3">VERY</span><span class="very imp" id="v4">IMPORTANT</span></div>'),
    (2, 118.7, 123.4, 'Experience <em>&gt;</em> Degree', ''),
    (3, 170.9, 175.4, 'Always <em>upskill</em>', ''),
    (4, 241.9, 249.3, 'Choose your <em>circle</em>', ''),
    (5, 291.0, 298.4, 'Love the job, <em>not the company</em>',
     '<div class="extra"><span class="lj y" id="lj1">&#9829; Your job</span><span class="lj n" id="lj2">&#10005; The company</span></div>'),
    (6, 355.0, 361.5, 'Always have a <em>backup plan</em>', ''),
    (7, 469.6, 476.8, 'Save money &amp; <em>invest</em>', ''),
]


def chapters_html():
    out = []
    for i, (num, txt, a, b) in enumerate(CHAPTERS):
        out.append(f'      <div id="ch{i}" class="clip chap" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="7">\n'
                   f'        <div class="tagbox"><span class="num">{num}</span><span class="txt">{txt}</span></div>\n      </div>')
    return "\n".join(out)


def captions_html():
    return "\n".join(
        f'      <div id="{cid}" class="clip" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="3">\n'
        f'        <div class="cap-wrap"><span class="cap">{html}</span></div>\n      </div>'
        for cid, a, b, ul, html in CAPS)


def slams_html():
    out = []
    for n, a, b, title, extra in SLAMS:
        dots = "".join(f'<i class="{"now" if k == n else ("on" if k < n else "")}"></i>' for k in range(1, 8))
        out.append(f'''      <div id="slam{n}" class="clip slam" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="1">
        <div class="panel">
          <div class="bar"></div>
          <span class="label">Hard lesson</span>
          <div class="big"><b>0{n}</b><span>/ 07</span></div>
          <span class="headline">{title}</span>
          <div class="dots">{dots}</div>
          {extra}
        </div>
      </div>''')
    return "\n".join(out)


def js_block():
    lines = ["      // ---------- chapters, captions, slams ----------"]
    for i, (_, _, a, b) in enumerate(CHAPTERS):
        lines.append(f'      chapter("#ch{i}", {a}, {b});')
    for cid, a, b, ul, _ in CAPS:
        lines.append(f'      caption("#{cid}", {a}, {b}, {ul});')
    for n, a, b, _, _ in SLAMS:
        lines.append(f'      slam("#slam{n}", {a}, {b});')
    lines += [
        '      [["#v1", 45.15], ["#v2", 46.14], ["#v3", 46.39], ["#v4", 46.78]].forEach(([s, t]) => tl.fromTo(s, { scale: 2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.5)" }, t));',
        '      tl.fromTo(["#v1", "#v2", "#v3"], { y: 0 }, { y: -6, duration: 0.15, yoyo: true, repeat: 3, ease: "sine.inOut", stagger: 0.1, immediateRender: false }, 49.35);',
        '      tl.fromTo("#lj1", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }, 294.78);',
        '      tl.fromTo("#lj2", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }, 296.3);',
        '      tl.fromTo("#lj2", { x: 0 }, { x: 6, duration: 0.06, yoyo: true, repeat: 5, ease: "none", immediateRender: false }, 296.7);',
    ]
    return "\n".join(lines)


# ---------------- camera track ----------------
EV = []  # (start, end, keyframes)
def punch(a, b, s, i=0.6, o=0.6):
    EV.append((a, b + o, [(a, s, i, "power2.inOut"), (b, 1, o, "power2.inOut")]))
def snap(t, s, rel, rd=0.5):
    EV.append((t, rel + rd, [(t, s, 0, ""), (rel, 1, rd, "power2.inOut")]))

punch(10.7, 15.9, 1.10, 1.2, 0.8)
punch(26.0, 29.8, 1.12)
snap(39.16, 1.15, 41.0)
EV.append((45.15, 48.2, [(45.15, 1.08, 0, ""), (46.14, 1.14, 0, ""), (46.39, 1.2, 0, ""), (47.6, 1, 0.6, "power2.inOut")]))
snap(49.35, 1.1, 51.2)
punch(90.3, 92.4, 1.12, 0.5)
snap(106.78, 1.2, 108.9)
snap(118.8, 1.15, 120.6)
punch(164.7, 168.2, 1.14)
snap(170.96, 1.15, 172.8)
snap(178.22, 1.12, 179.4)
punch(202.8, 208.9, 1.12, 0.6, 0.7)
snap(220.36, 1.18, 222.4)
punch(233.7, 239.3, 1.22, 0.8, 0.7)
snap(241.98, 1.15, 243.8)
punch(252.6, 256.5, 1.12)
punch(285.4, 288.0, 1.14, 0.5)
snap(293.23, 1.15, 295.2)
punch(298.6, 300.9, 1.12, 0.4)
punch(320.6, 323.8, 1.22, 0.7)
snap(332.17, 1.18, 334.4)
punch(335.4, 342.3, 1.12)
snap(357.26, 1.15, 359.2)
snap(384.08, 1.22, 385.6)
punch(397.1, 403.9, 1.14)
punch(409.8, 414.2, 1.10)
snap(427.72, 1.18, 428.8)
snap(469.91, 1.15, 471.8)
punch(478.0, 481.9, 1.14, 0.4)
snap(488.39, 1.15, 489.6)
snap(499.48, 1.15, 500.4)
punch(515.0, 517.8, 1.14, 0.5)
punch(548.3, 550.6, 1.14, 0.5)
punch(569.0, 574.6, 1.08, 0.8, 0.8)
EV.sort()
for (a1, e1, _), (a2, _, _) in zip(EV, EV[1:]):
    assert e1 <= a2 + 1e-6, f"camera overlap {a1}-{e1} vs {a2}"

CAM, cursor, flip = [], 0.0, 0
def fill(a, b):
    """Slow push/pull cycles (max 1.07) through a static gap."""
    global flip
    gap = b - a
    if gap < 4: return
    cycles = max(1, round(gap / 16))
    seg = gap / cycles
    for k in range(cycles):
        s0 = a + k * seg
        half = (seg - 0.2) / 2
        peak = (1.06, 1.07, 1.05)[flip % 3]; flip += 1
        CAM.append((round(s0 + 0.1, 2), peak, round(half, 2), "sine.inOut"))
        CAM.append((round(s0 + 0.1 + half, 2), 1, round(half, 2), "sine.inOut"))
for a, e, kfs in EV:
    fill(cursor, a)
    CAM.extend(kfs)
    cursor = e
fill(cursor, 578.4)
CAM_JS = json.dumps([[t, s, d, e] for t, s, d, e in CAM])
moving = sum(min(d, 30) for _, _, d, _ in CAM) + sum(max(0, b - a) for a, b, _ in EV)

# ---------------- sound effects ----------------
DUR = {"whoosh-1": 0.45, "whoosh-2": 0.23, "whoosh-3": 0.43, "whoosh-4": 0.39, "whoosh-5": 0.37,
       "whoosh-7": 0.67, "tick": 0.06, "pop": 0.15, "ding": 1.1, "impact": 0.6, "heartbeat": 0.6}
for c in json.load(open(f"{LIB}/catalog.json")):
    DUR[c["file"][:-4]] = c["duration"]
POPS = ["30-blip-pop", "43-click-tonal", "60-blip-tonal"]
_p = [0]
def pop():
    _p[0] += 1
    return POPS[(_p[0] - 1) % 3]
INS = ["whoosh-3", "whoosh-4", "whoosh-5"]
_w = [0]
def win():
    _w[0] += 1
    return INS[(_w[0] - 1) % 3]

SFX = [
    (0.0, "08-boom-swoosh", 0.4, "intro swipe"), (1.25, "whoosh-5", 0.32, "roles in"),
    (2.95, "03-bell-high", 0.25, "12 years"), (9.3, "24-ding-ring", 0.22, "top step flag"), (10.65, "whoosh-3", 0.32, "lower third in"), (16.1, "whoosh-2", 0.2, "lower third out"),
]
SFX += [(1.6 + 0.1 * i, "49-click-tiny", 0.22, f"year tick {i+1}") for i in range(12)]
SFX += [(t, pop(), 0.32, "role") for t in (3.16, 4.37, 6.43, 8.89)]
# panels in/out (track-1 panels listed with in/out)
PANELS = [(103.8, 109.0), (109.9, 118.6), (129.9, 156.4), (164.6, 170.5), 
          (344.0, 354.6), (367.0, 383.6), (456.0, 467.4), (500.7, 507.4), (511.7, 518.6),
          (536.9, 547.6), (548.3, 556.8), (557.2, 568.8)]
for a, b in PANELS:
    SFX += [(round(a - 0.05, 2), win(), 0.32, "panel in"), (round(b - 0.45, 2), "whoosh-2", 0.2, "panel out")]
for n, a, b, _, _ in SLAMS:
    SFX += [(a, "06-impact-punch", 0.3, f"lesson {n} slam"), (round(a - 0.05, 2), "45-swish-short", 0.3, f"lesson {n} swish"),
            (round(b - 0.45, 2), "whoosh-2", 0.2, f"lesson {n} out")]
for _, _, a, _ in CHAPTERS:
    SFX.append((a, "49-click-tiny", 0.32, "chapter"))
for a, b, kfs in EV:
    if kfs[0][2] > 0 and a > 20:
        SFX.append((round(a - 0.05, 2), "45-swish-short", 0.26, "punch-in"))
SFX += [
    # L1
    (45.15, "impact", 0.3, "VERY 1"), (46.14, "impact", 0.3, "VERY 2"), (46.39, "impact", 0.32, "VERY 3"),
    (46.78, "03-bell-high", 0.25, "IMPORTANT"),
    (104.2, "12-blip-double", 0.3, "robot"), (105.42, "43-click-tonal", 0.3, "bubble 1"), (106.78, "30-blip-pop", 0.32, "Hoy Chad"),
    (112.8, pop(), 0.3, "2013"), (114.7, pop(), 0.3, "2026"), (116.28, "03-bell-high", 0.25, "ideas bulb"),
    # L2
    (130.2, pop(), 0.28, "diploma"), (134.6, "26-hit-short", 0.26, "diploma strike"),
    (138.0, "43-click-tonal", 0.28, "q1"), (139.85, "30-blip-pop", 0.28, "q2"), (142.0, "43-click-tonal", 0.28, "q3"),
    (144.06, "30-blip-pop", 0.28, "q4"), (147.81, "43-click-tonal", 0.28, "q5"),
    (165.2, "50-thump-short", 0.3, "scale tips"),
    # L3
    (178.22, "45-swish-short", 0.24, "snap"),
    (220.36, "45-swish-short", 0.26, "not for you snap"),
    # L4
    (265.43, pop(), 0.32, "youtube"), (266.46, pop(), 0.32, "facebook"),
    (286.26, "40-boing-down", 0.22, "put down X"),
    # L5
    (294.78, "03-bell-high", 0.25, "love job"), (296.3, "26-hit-short", 0.28, "not company"), (298.88, "06-impact-punch", 0.35, "HARD RULE"),
    (322.23, "impact", 0.3, "replaceable"), (332.17, "26-hit-short", 0.28, "you're out"),
    (344.4, pop(), 0.3, "you"), (346.08, pop(), 0.3, "client A"), (346.68, pop(), 0.3, "client B"), (347.28, pop(), 0.3, "client C"),
    # L6
    (368.15, "30-blip-pop", 0.3, "VA pillar"), (369.64, pop(), 0.26, "? 1"), (369.94, pop(), 0.26, "? 2"),
    (380.25, "28-bloop-low", 0.3, "pillar falls"), (384.08, "47-vocal-wow", 0.28, "nganga"),
    (427.72, "45-swish-short", 0.26, "utak snap"),
    (458.46, "28-bloop-low", 0.3, "VA drops"), (462.3, "29-bloop-low-2", 0.28, "taas-baba"), (465.18, "24-ding-ring", 0.25, "side income"),
    # L7
    (478.0, "06-impact-punch", 0.35, "HARD RULE 2"), (488.39, "45-swish-short", 0.24, "nakakalimot"), (499.48, "45-swish-short", 0.24, "nakakalimot 2"),
    (502.01, pop(), 0.3, "gastos"), (503.28, pop(), 0.3, "labas"), (505.08, pop(), 0.3, "bakasyon"),
    (512.0, pop(), 0.3, "piggy"), (513.0, "03-bell-high", 0.25, "coin"), (513.88, "24-ding-ring", 0.22, "growth"), (515.36, pop(), 0.3, "umbrella"),
    (538.07, "29-bloop-low-2", 0.28, "tumal dip"), (544.59, "24-ding-ring", 0.25, "prepared shield"),
    (553.2, "03-bell-high", 0.25, "jar coin 1"), (553.75, "03-bell-high", 0.22, "jar coin 2"),
    # recap + cta + end
] + [(round(558.6 + i * 0.45, 2), "43-click-tonal", 0.3, f"recap {i+1}") for i in range(7)] + [
    (561.6, "24-ding-ring", 0.25, "recap done"),
    (569.0, "whoosh-3", 0.3, "cta in"), (569.78, "43-click-tonal", 0.4, "like"), (571.3, "43-click-tonal", 0.4, "subscribe"),
    (571.38, "24-ding-ring", 0.26, "subscribed"), (574.95, "whoosh-2", 0.2, "cta out"),
    (579.55, "whoosh-7", 0.5, "end wipe"), (580.2, "whoosh-1", 0.25, "thanks"),
    (581.0, "impact", 0.3, "slam 1"), (581.35, "impact", 0.3, "slam 2"), (581.7, "impact", 0.3, "slam 3"),
    (582.1, "55-orchestra-hit-sparkle", 0.25, "wordmark"),
]


# ---------------- sketch boards (Style B): whoosh in/out + pencil on DRAWINGS only (0.15) ----------------
BOARDS = [(62.4, 85.4), (190.4, 217.2), (269.1, 289.0), (432.4, 455.8)]
for a, b_ in BOARDS:
    SFX += [(round(a - 0.05, 2), "whoosh-3", 0.3, "sketch board in"), (round(b_ - 0.45, 2), "whoosh-2", 0.2, "sketch board out")]
DRAWS = [(64.3, 0.55), (71.76, 0.8), (75.5, 0.8), (78.5, 0.65), (84.0, 0.4),
         (202.2, 0.8), (206.0, 0.8), (210.82, 1.42),
         (272.4, 0.85), (280.43, 1.42), (284.19, 0.85), (285.5, 0.45), (286.26, 0.4),
         (433.07, 0.85), (439.13, 0.85), (444.06, 0.85), (446.9, 0.85)]
for i, (t, d) in enumerate(DRAWS):
    SFX.append((t, "pencil" if i % 2 == 0 else "pencil-rev", 0.15, "pencil (drawing)"))
    DUR.setdefault("pencil", 1.422); DUR.setdefault("pencil-rev", 1.422)
PENCIL_LEN = {t: d for t, d in DRAWS}

POOL = [9, 10, 11, 12, 13, 14] + list(range(18, 34))
SFX_DIR = os.path.join(os.path.dirname(os.path.abspath(OUT)), "assets/sfx")
lines, last_end = [], {tr: -1 for tr in POOL}
for n, (t, s, v, note) in enumerate(sorted(SFX), 1):
    if s[:2].isdigit() and not os.path.exists(f"{SFX_DIR}/{s}.wav"):
        shutil.copy(f"{LIB}/{s}.wav", f"{SFX_DIR}/{s}.wav")
    d = min(DUR[s], ROOT_END - t, PENCIL_LEN.get(t, 99) if s.startswith("pencil") else 99)
    tr = next(tr for tr in POOL if last_end[tr] <= t + 1e-6)
    last_end[tr] = t + d
    lines.append(f'      <audio id="sfx-{n:03d}" src="assets/sfx/{s}.wav" data-start="{t}" data-duration="{d:.3f}" data-volume="{v}" data-track-index="{tr}"></audio> <!-- {note} -->')

HIDE = [[a, b] for _, a, b, _, _ in CAPS]
cues = json.load(open(f"{S}/cues.json"))
for c in cues:
    c["e"] = min(c["e"], SUB_END)

html = open(f"{S}/template.html").read()
for k, v in {"__AUDIO__": "\n".join(lines), "__CHAPTERS__": chapters_html(), "__CAPTIONS__": captions_html(),
             "__SLAMS__": slams_html(), "__JS__": js_block(), "__CAM__": CAM_JS,
             "__CUES__": json.dumps(cues, ensure_ascii=False), "__HIDE__": json.dumps(HIDE)}.items():
    assert k in html, k
    html = html.replace(k, v)
open(OUT, "w").write(html)
static = 0.0
prev = 0.0
for t, s, d, e in CAM:
    pass
print(f"{len(lines)} sfx, {len(cues)} cues, {len(CAM)} camera keyframes, {len(EV)} punch/snap moves, tracks used {max(t for t in last_end if last_end[t] > 0)}")
