#!/usr/bin/env python3
"""Composition generator for "7 Ways How Virtual Assistants Earn Using HighLevel" (2026-11-06).

Reuses CSS + JS helpers from the video-editor skill's lesson-video-template.html, adds this video's
own panels (experience meter, path slams, trail map, automation flow, 3 sketch boards...).
usage: python3 build_7ways.py hf-project/index.html <cues.json>
"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes as SC  # skill copy: scripts/scenes.py (project copy was scenes_7ways.py)

OUT, CUES = sys.argv[1], sys.argv[2]
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this skill folder
LIB = os.environ.get("SFX_LIB", os.path.expanduser("~/sfx-library"))  # your leveled SFX library folder
FOOT = 817.63
ROOT = 820.7
SUB_END = 817.6

tpl = open(f"{SK}/templates/lesson-video-template.html").read()
CSS = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
tl_lines = tpl.split("\n")
i0 = next(i for i, l in enumerate(tl_lines) if "// ---------- helpers" in l)
i1 = next(i for i, l in enumerate(tl_lines) if "// ---------- Board 1" in l)
HELPERS = "\n".join(l for l in tl_lines[i0:i1] if "tornEdge(`${id} .paper`" not in l)
bc = open(f"{SK}/broll-cutaway.html").read()
BR_CSS = re.search(r"<style>\n(.*?)</style>", bc, re.S).group(1)
BR_JS = re.search(r"<script>(.*?)brollCut\(\"#br-data-entry\"", bc, re.S).group(1)

ease = "power3.out"
H = []   # html blocks
J = []   # js lines
SFX = [] # (t, clip, vol, note)
CAPS, EV = [], []

# ---------------------------------------------------------------- chapters
CHAPTERS = [
    ("00", "INTRO", 16.2, 66.2),
    ("1", "PATH 1 &middot; GHL VA FOR HIRE", 76.7, 125.3),
    ("2", "PATH 2 &middot; ONBOARDING SUPPORT", 125.5, 188.3),
    ("3", "PATH 3 &middot; SOCIAL MEDIA VA", 188.5, 249.9),
    ("4", "PATH 4 &middot; AUTOMATION BUILDER", 250.1, 444.0),
    ("5", "PATH 5 &middot; SUCCESS MANAGER", 444.2, 560.8),
    ("6", "PATH 6 &middot; HIGHLEVEL AFFILIATE", 561.0, 649.4),
    ("7", "PATH 7 &middot; YOUR OWN SAAS", 649.6, 730.5),
    ("&#10003;", "RECAP", 730.7, 741.4),
    ("&#9733;", "CHAD AI COMMUNITY", 741.6, 817.4),
]
for i, (num, txt, a, b) in enumerate(CHAPTERS):
    H.append(f'<div id="ch{i}" class="clip chap" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="7"><div class="tagbox"><span class="num">{num}</span><span class="txt">{txt}</span></div></div>')
    J.append(f'chapter("#ch{i}", {a}, {b});')
    SFX.append((a, "49-click-tiny", 0.3, "chapter"))

# ---------------------------------------------------------------- main-point captions
def cap(cid, a, b, ul, html, s=1.14, i=0.6, o=0.6):
    CAPS.append((cid, a, b, ul, html))
    EV.append((a, b - 0.4 + o, [(a, s, i, "power2.inOut"), (b - 0.4, 1, o, "power2.inOut")]))
    SFX.append((round(a - 0.05, 2), "45-swish-short", 0.24, "punch-in"))
cap("ckeme", 16.0, 21.7, 20.63, 'Seven actual ways to earn as a VA using GHL, <b>na hindi keme lang<i class="ul"></i></b>.', 1.14)
cap("clowest", 82.3, 84.8, 82.95, 'This is the <b>lowest bar<i class="ul"></i></b> to enter.', 1.12, 0.5)
cap("cpay", 115.5, 117.5, 116.03, 'Someone is <b>paying you<i class="ul"></i></b> to get better.', 1.12, 0.4)
cap("cvoice", 234.5, 238.3, 237.45, 'Strategically reading <b>the voice of the market<i class="ul"></i></b>.', 1.14)
cap("chighly", 255.7, 260.6, 258.9, 'Digging na for the <b>highly paid<i class="ul"></i></b> stuff.', 1.12)
cap("crate", 333.7, 337.8, 336.4, 'Once you can build that automation, <b>your rate goes up<i class="ul"></i></b>.', 1.14)
cap("cvaluable", 360.3, 364.0, 361.95, '<b>Super valuable<i class="ul"></i></b> ka talaga sa market.', 1.18)
cap("cgold", 373.2, 375.6, 374.6, 'Time is <b>gold<i class="ul"></i></b>, di ba?', 1.12, 0.4)
cap("cinvest", 438.3, 443.8, 438.68, 'If you <b>invest in yourself<i class="ul"></i></b>, you can become an automation specialist.', 1.14)
cap("conetime", 494.6, 497.6, 496.3, 'It\'s not a <b>one-time setup<i class="ul"></i></b>.', 1.18)
cap("cbeginner", 661.1, 663.5, 662.63, 'Hindi ito para sa mga <b>beginner VAs<i class="ul"></i></b> lang.', 1.14, 0.5)
cap("clink", 806.9, 810.6, 807.7, 'Check the <b>link down below<i class="ul"></i></b>.', 1.12)
for cid, a, b, ul, html in CAPS:
    H.append(f'<div id="{cid}" class="clip" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="3"><div class="cap-wrap"><span class="cap">{html}</span></div></div>')
    J.append(f'caption("#{cid}", {a}, {b}, {ul});')

# ---------------------------------------------------------------- camera snaps
def snap(t, s, rel, rd=0.5, sfx="45-swish-short"):
    EV.append((t, rel + rd, [(t, s, 0, ""), (rel, 1, rd, "power2.inOut")]))
    if sfx: SFX.append((round(t - 0.03, 2), sfx, 0.24, "snap"))
snap(51.23, 1.15, 53.0)
snap(289.38, 1.18, 290.8, sfx=None)
snap(339.8, 1.18, 341.6, sfx=None)
snap(397.12, 1.2, 398.6, sfx=None)
snap(410.78, 1.22, 412.3, sfx=None)
snap(689.46, 1.15, 691.0)
EV.append((107.9, 112.0, [(107.9, 1.14, 0.5, "power2.inOut"), (111.4, 1, 0.6, "power2.inOut")]))

# ---------------------------------------------------------------- path slams (experience meter)
PATHS = [(1, 76.62, 82.2, 'GHL VA <em>for hire</em>', "Lowest bar to enter"),
         (2, 125.46, 131.0, 'GHL onboarding <em>support</em>', "Set clients up right"),
         (3, 188.4, 194.0, 'Social media VA <em>inside GHL</em>', "Planner + community"),
         (4, 250.0, 255.6, 'Automation <em>builder</em>', "Real platform knowledge"),
         (5, 444.1, 451.2, 'GHL success <em>manager</em>', "Ongoing, not one-time"),
         (6, 561.0, 567.2, 'HighLevel <em>affiliate</em>', "Recurring commission"),
         (7, 649.6, 657.0, 'Your own <em>SaaS</em> agency', "Highest bar &middot; big capital")]
def meter(n, cls="m"):
    out = []
    for k in range(1, 8):
        h = 18 + k * 9
        c = "now" if k == n else ("on" if k < n else "")
        out.append(f'<i class="{c}" style="height:{h}px"></i>')
    return f'<div class="meter {cls}">{"".join(out)}</div>'
PKEYS = {1: ("contacts", "FOR HIRE"), 2: ("onboard", None), 3: ("socialphone", None), 4: ("workflow", None), 5: ("clients", None), 6: ("coins", None), 7: ("saas", None)}
for n, a, b, title, sub in PATHS:
    key, st = PKEYS[n]
    SC.pscene(H, J, SFX, n, a, b, title.replace("<em>", "<em>").replace("</em>", "</em>"), sub, key, st)

# ---------------------------------------------------------------- panels (right side)
PANELS = []
def panel(pid, a, b, inner, track=1, head=True, extra_cls=""):
    H.append(f'<div id="{pid}" class="clip {extra_cls}" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{track}"><div class="panel"><div class="bar"></div>{inner}</div></div>')
    J.append(f'panelIn("#{pid}", {a}, {str(head).lower()}); panelOut("#{pid}", {b});')
    PANELS.append((a, b))

def items(pid, rows, times, label_n=None):
    html = '<div class="items">' + "".join(
        f'<div class="item" id="{pid}-{k}"><span class="n">{label_n[k] if label_n else k+1}</span><span class="t">{r}</span></div>'
        for k, r in enumerate(rows)) + "</div>"
    js = [f'tl.set("#{pid} .item", {{ opacity: 0.25 }}, {times[0]-1.2});'] + [f'itemOn("#{pid}-{k}", {t});' for k, t in enumerate(times)]
    for t in times: SFX.append((t, POP(), 0.28, f"{pid} item"))
    return html, js

_p = [0]
def POP():
    _p[0] += 1
    return ["30-blip-pop", "43-click-tonal", "60-blip-tonal"][(_p[0] - 1) % 3]

# 1) intro hub (HighLevel logo + connected tiles) 0.35 -> 9.0
import math
SC.hub(H, J, SFX)
SC.kinetic(H, J, SFX)

# 2) experience meter intro 21.9 -> 31.5
bars = "".join(f'<rect class="eb" id="eb{k}" x="{14+k*52}" y="{190-(30+k*22)}" width="40" height="{30+k*22}" rx="8" fill="{["#1e3a8a","#1e40af","#1d4ed8","#2563EB","#3882F6","#60a5fa","#EAF3FF"][k]}"/>' for k in range(7))
panel("emeter", 21.9, 31.4, f'''<span class="label">Ranked by experience</span>
<span class="headline">Which path <em>fits you?</em></span>
<svg class="viz" width="376" height="232" viewBox="0 0 376 232">{bars}
<line x1="6" y1="196" x2="370" y2="196" stroke="rgba(234,243,255,0.4)" stroke-width="3"/>
<text id="em-lo" x="10" y="224" font-size="15" fill="#EAF3FF">LOWEST</text><text id="em-hi" x="366" y="224" font-size="15" fill="#EAF3FF" text-anchor="end">HIGHEST</text></svg>''')
J.append('''for (let k = 0; k < 7; k++) tl.fromTo("#eb" + k, { scaleY: 0, svgOrigin: "0 190" }, { scaleY: 1, svgOrigin: "0 190", duration: 0.35, ease: "back.out(1.8)" }, 22.2 + k * 0.33);
tl.fromTo("#em-lo", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 22.11);
tl.fromTo("#em-hi", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 24.28);''')
SFX += [(21.85, "whoosh-4", 0.3, "meter in")] + [(round(22.2 + k * 0.33, 2), "49-click-tiny", 0.22, "bar") for k in range(7)] + [(24.4, "03-bell-high", 0.2, "highest")]

# 3) lower third 32.2 -> 38.0
H.append('''<div id="lower" class="clip" data-start="32.2" data-duration="3.8" data-track-index="2"><div class="lt"><div class="lt-accent"></div><div class="lt-body">
<span class="name">Chad <em>Godoy</em></span><span class="role">VA FOR 12 YEARS &bull; GHL CERTIFIED ADMIN &bull; CHADGODOY.IO</span><div class="shine" id="lt-shine"></div></div></div></div>''')
J.append('''tl.fromTo("#lower .lt", { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease }, 32.2);
tl.fromTo("#lower .lt-body", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.7, ease }, 32.35);
tl.fromTo("#lt-shine", { x: -140 }, { x: 900, duration: 0.9, ease: "power2.inOut" }, 33.2);
tl.to("#lower .lt", { x: -40, opacity: 0, duration: 0.4, ease: "power2.in" }, 35.6);''')
SFX += [(32.15, "whoosh-3", 0.3, "lower third in"), (35.6, "whoosh-2", 0.2, "lower third out")]
EV.append((32.3, 36.0, [(32.3, 1.1, 1.2, "power2.inOut"), (35.4, 1, 0.6, "power2.inOut")]))
SC.confused(H, J, SFX)

# 5) trail map 66.5 -> 76.3
br = ""
for k in range(7):
    y = 22 + k * 40
    br += f'<path class="trail" id="tr{k}" d="M40 150 C 140 150, 170 {y}, 300 {y}" fill="none" stroke="#3882F6" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    br += f'<g class="sign" id="sg{k}"><circle cx="318" cy="{y}" r="16" fill="#2563EB" stroke="#EAF3FF" stroke-width="3"/><text x="318" y="{y+6}" font-size="16" fill="#fff" text-anchor="middle">{k+1}</text></g>'
panel("trail", 66.5, 76.3, f'''<span class="label">Choose your own adventure</span>
<span class="headline">7 paths, <em>7 ways</em></span>
<svg class="viz" width="376" height="300" viewBox="0 0 376 300">{br}
<g id="you"><circle cx="40" cy="150" r="24" fill="#FFC531" stroke="#0B2058" stroke-width="4"/><text x="40" y="156" font-size="14" fill="#0B2058" text-anchor="middle">YOU</text></g></svg>
<span class="psub" id="trail-q">Find the one that <b>matches your level</b></span>''')
J.append('''tl.fromTo("#you", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.45, ease: "back.out(2)" }, 66.9);
for (let k = 0; k < 7; k++) { tl.fromTo("#tr" + k, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 68.42 + k * 0.17); tl.fromTo("#sg" + k, { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.35, ease: "back.out(2.5)" }, 68.8 + k * 0.17); }
tl.fromTo("#trail-q", { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease }, 72.3);''')
SFX += [(66.45, "whoosh-3", 0.3, "trail in"), (66.9, "30-blip-pop", 0.3, "you")] + [(round(68.8 + k * 0.17, 2), "49-click-tiny", 0.22, "sign") for k in range(7)] + [(72.3, "43-click-tonal", 0.26, "match")]

# 6) GHL VA tasks 93.0 -> 105.9 (illustrated)
SC.stage(H, J, SFX, "tasks", 93.0, 105.9, "GHL VA day-to-day", [
    ("contacts", "Update contacts", 93.29, None), ("mail", "Email campaigns", 94.97, None),
    ("calendar", "Basic tasks", 96.89, None), ("traits", "What you need", 101.7, (101.9, 102.9, 104.3))])
PANELS.append((93.0, 105.9))

# 7) rate tag 106.3 -> 112.0
panel("rate1", 106.3, 112.0, '''<span class="label">Starting rate</span>
<div class="price"><b id="r1n">$10&ndash;15</b><span>/ hour</span></div>
<span class="stampin" id="r1s">That's real money</span>''', head=False)
J.append('popIn("#r1n", 107.93); tl.fromTo("#r1s", { scale: 2, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -4, duration: 0.35, ease: "back.out(2.2)" }, 111.1);')
SFX += [(106.25, "whoosh-5", 0.3, "rate in"), (107.93, "06-impact-punch", 0.3, "rate"), (111.1, "26-hit-short", 0.26, "real money")]

# 8) onboarding 166.0 -> 177.2 (illustrated)
SC.stage(H, J, SFX, "onb", 166.0, 177.2, "Onboarding setup", [
    ("bizinfo", "Business info", 167.64, None), ("branding", "Branding", 170.17, None),
    ("socialacc", "Social accounts", 171.1, None), ("apps", "Third-party apps", 172.58, None)])
PANELS.append((166.0, 177.2))

# 9) social planner 195.4 -> 207.3 (illustrated)
SC.stage(H, J, SFX, "pln", 195.4, 207.3, "Built into GHL", [
    ("platforms", "Social Planner", 197.0, None), ("writeposts", "Write posts", 201.97, None),
    ("schedule", "Schedule content", 202.9, None), ("create", "Create content", 203.92, None)])
PANELS.append((195.4, 207.3))

# 10) market data 238.4 -> 244.0
panel("mkt", 238.4, 244.0, '''<span class="label">Voice of the market</span>
<div class="bubbles"><span class="bub" id="mb1">Magkano po ito?</span><span class="bub alt" id="mb2">Available pa po?</span><span class="bub" id="mb3">Paano mag-book?</span></div>
<div class="chips"><span class="chip tag" id="mt1">#interested</span><span class="chip tag" id="mt2">#pricing</span><span class="chip tag" id="mt3">#hot-lead</span></div>
<svg class="viz" width="376" height="90" viewBox="0 0 376 90"><rect class="bb" id="bb1" x="20" y="40" width="70" height="46" rx="6" fill="#3882F6"/><rect class="bb" id="bb2" x="110" y="14" width="70" height="72" rx="6" fill="#2563EB"/><rect class="bb" id="bb3" x="200" y="28" width="70" height="58" rx="6" fill="#60a5fa"/><rect class="bb" id="bb4" x="290" y="4" width="70" height="82" rx="6" fill="#EAF3FF"/></svg>''', head=False)
J.append('''["#mb1","#mb2","#mb3"].forEach((s,k) => popIn(s, 238.6 + k * 0.35));
["#mt1","#mt2","#mt3"].forEach((s,k) => popIn(s, 240.5 + k * 0.2));
for (let k = 1; k <= 4; k++) tl.fromTo("#bb" + k, { scaleY: 0, svgOrigin: "0 86" }, { scaleY: 1, svgOrigin: "0 86", duration: 0.4, ease: "back.out(1.8)" }, 241.67 + k * 0.12);''')
SFX += [(238.35, "whoosh-5", 0.3, "mkt in"), (238.6, "43-click-tonal", 0.26, "bubble"), (238.95, "30-blip-pop", 0.26, "bubble"), (239.3, "43-click-tonal", 0.26, "bubble"),
        (240.5, "49-click-tiny", 0.26, "tag"), (240.7, "49-click-tiny", 0.26, "tag"), (240.9, "49-click-tiny", 0.26, "tag"), (241.8, "24-ding-ring", 0.22, "data")]

# 11) automation flow A 265.2 -> 273.2, flow B 279.2 -> 306.8
def flow(pid, a, b, lit_at):
    nodes = [("FORM", "Lead fills a form"), ("SMS", "Text sent right away"), ("PIPELINE", "Booked call tracked"), ("EMAIL", "Freebie delivered")]
    rows = "".join(f'<div class="fnode" id="{pid}-n{k}"><span class="fk">{n}</span><span class="ft">{t}</span></div>' + ('<i class="farrow"></i>' if k < 3 else "") for k, (n, t) in enumerate(nodes))
    panel(pid, a, b, f'<span class="label">Workflow</span><span class="headline">It runs <em>automatically</em></span><div class="flow">{rows}</div><span class="stampin" id="{pid}-auto">Automated na!</span>')
    J.append(f'tl.set("#{pid} .fnode", {{ opacity: 0.3 }}, {a});')
    for k, t in enumerate(lit_at):
        if t is None: continue
        J.append(f'tl.fromTo("#{pid}-n{k}", {{ opacity: 0.3, x: 24 }}, {{ opacity: 1, x: 0, duration: 0.4, ease, immediateRender: false }}, {t}); tl.set("#{pid}-n{k}", {{ className: "fnode on" }}, {t});')
        SFX.append((t, POP(), 0.28, f"{pid} node"))
    J.append(f'tl.set("#{pid}-auto", {{ opacity: 0 }}, {a});')
flow("flowa", 265.2, 273.2, [268.7, None, None, None])
flow("flowb", 279.2, 306.8, [279.6, 284.46, 292.99, 301.2])
J.append('tl.fromTo("#flowb-auto", { scale: 2, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -4, duration: 0.35, ease: "back.out(2.2)", immediateRender: false }, 289.38);')
SFX += [(265.15, "whoosh-3", 0.3, "flow in"), (272.75, "whoosh-2", 0.2, "flow out"), (279.15, "whoosh-4", 0.3, "flow in"), (289.38, "06-impact-punch", 0.3, "automated na"), (306.35, "whoosh-2", 0.2, "flow out")]

# 12) rate 2 337.9 -> 343.6
panel("rate2", 337.9, 343.6, '''<span class="label">Automation builder rate</span>
<div class="price old" id="r2o"><b>$10&ndash;15</b><span>/ hour</span><i class="pstrike" id="r2x"></i></div>
<div class="price"><b id="r2n">$20&ndash;50</b><span>/ hour</span></div>''', head=False)
J.append('tl.fromTo("#r2x", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 339.3); popIn("#r2n", 339.8);')
SFX += [(337.85, "whoosh-5", 0.3, "rate2 in"), (339.3, "26-hit-short", 0.24, "strike"), (339.8, "06-impact-punch", 0.32, "$20-50"), (343.15, "whoosh-2", 0.2, "rate2 out")]

# 13) automation wins 375.8 -> 386.4 (illustrated)
SC.stage(H, J, SFX, "wins", 375.8, 386.4, "Kaya mo i-automate", [
    ("leads", "Gathering leads", 376.85, None), ("mail", "Email campaigns", 378.31, None),
    ("booking", "Booking calendars", 379.78, None), ("followup", "Follow-up texts", 381.35, None)],
    tail_html='<span class="stampin" id="wins-a">Automated!</span>',
    tail_js=['tl.fromTo("#wins-a", { scale: 2, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -4, duration: 0.35, ease: "back.out(2.2)" }, 385.04);'])
SFX += [(385.04, "24-ding-ring", 0.24, "automated")]
PANELS.append((375.8, 386.4))

# 14) caveat stamp 395.4 -> 399.9
H.append('<div id="stcav" class="clip stamp" data-start="395.4" data-duration="4.5" data-track-index="4"><div class="st" id="stcav-s">CAVEAT?<small>&ldquo;KABYET&rdquo;</small></div></div>')
J.append('stamp("#stcav-s", 395.44, 399.9);')
SFX += [(395.44, "26-hit-short", 0.28, "caveat stamp"), (397.12, "40-boing-down", 0.24, "kabyet"), (410.78, "40-boing-down", 0.24, "high level pa")]

# 15) HLA card 422.2 -> 428.4
H.append('''<div id="ref-hla" class="clip ref" data-start="422.2" data-duration="6.2" data-track-index="16"><div class="card">
<div class="glow"></div>
<svg class="img icon" viewBox="0 0 200 200" width="230" height="230"><polygon points="100,40 190,80 100,120 10,80" fill="#2563EB" stroke="#EAF3FF" stroke-width="6" stroke-linejoin="round"/><path d="M50 100 L50 140 C70 160 130 160 150 140 L150 100" fill="#1e40af" stroke="#EAF3FF" stroke-width="6"/><line x1="176" y1="86" x2="176" y2="140" stroke="#FFC531" stroke-width="7"/><circle cx="176" cy="146" r="9" fill="#FFC531"/></svg>
<div class="tag"><span class="name">HighLevel Accelerator</span><span class="sub">HLA community</span></div>
<div class="tag t2" id="hla-cert"><span class="name sm">&#10003; GHL Certified Admin</span></div>
</div></div>''')
J.append('refCard("#ref-hla", 422.2, 428.4); tl.fromTo("#hla-cert", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease, immediateRender: false }, 425.68);')
SFX += [(422.2, "30-blip-pop", 0.32, "HLA card"), (425.68, "24-ding-ring", 0.22, "certified")]

# 16) Liz card 465.5 -> 472.4 and 548.8 -> 554.4
H.append('''<div id="ref-liz" class="clip ref" data-start="465.5" data-duration="6.9" data-track-index="16"><div class="card">
<div class="glow"></div><img class="img portrait" src="assets/refs/liz-manalo.jpg" alt="Liz Manalo" />
<div class="tag"><span class="name">Liz Manalo</span><span class="sub">GHL Success Manager</span></div></div></div>
<div id="ref-liz2" class="clip ref" data-start="548.8" data-duration="5.6" data-track-index="16"><div class="card">
<div class="glow"></div><img class="img portrait sm" src="assets/refs/liz-manalo.jpg" alt="Liz Manalo" />
<div class="tag"><span class="name">Follow Ms. Liz</span><span class="sub">Links in the description &darr;</span></div></div></div>''')
J.append('refCard("#ref-liz", 465.5, 472.4); refCard("#ref-liz2", 548.8, 554.4);')
SFX += [(465.5, "30-blip-pop", 0.32, "Liz card"), (548.8, "43-click-tonal", 0.3, "Liz card 2")]

# 17) weekly check-in 479.6 -> 488.8
days = ["MON", "TUE", "WED", "THU", "FRI"]
panel("chk", 479.6, 488.8, f'''<span class="label">Success manager</span><span class="headline">Weekly <em>check-ins</em></span>
<div class="days">{"".join(f'<div class="day" id="dy{k}"><span>{d}</span><i id="dk{k}">&#10003;</i></div>' for k, d in enumerate(days))}</div>
<div class="item good" id="chk-ok"><span class="n">&#10003;</span><span class="t">No client stuck</span></div>''')
J.append('for (let k = 0; k < 5; k++) popIn("#dk" + k, 481.62 + k * 0.22); popIn("#chk-ok", 484.52);')
SFX += [(479.55, "whoosh-4", 0.3, "chk in")] + [(round(481.62 + k * 0.22, 2), "49-click-tiny", 0.24, "day tick") for k in range(5)] + [(484.52, "24-ding-ring", 0.22, "not stuck"), (488.35, "whoosh-2", 0.2, "chk out")]

# 18) gift 590.6 -> 603.8
panel("gift", 590.6, 603.8, '''<span class="label">My affiliate link</span><span class="headline">Libreng <em>30 days</em></span>
<svg class="viz" width="376" height="220" viewBox="0 0 376 220"><rect x="108" y="96" width="160" height="116" rx="10" fill="#2563EB" stroke="#EAF3FF" stroke-width="4"/><rect x="178" y="96" width="20" height="116" fill="#FFC531"/>
<g id="lid"><rect x="96" y="66" width="184" height="36" rx="8" fill="#3882F6" stroke="#EAF3FF" stroke-width="4"/><rect x="178" y="66" width="20" height="36" fill="#FFC531"/></g>
<g id="g30"><circle cx="188" cy="40" r="34" fill="#FFC531" stroke="#0B2058" stroke-width="4"/><text x="188" y="50" font-size="28" fill="#0B2058" text-anchor="middle" font-family="Poppins">30</text></g></svg>
<span class="psub">Head start bago magbayad</span>''')
J.append('''tl.set("#g30", { opacity: 0 }, 590.6);
tl.fromTo("#lid", { y: 0, rotation: 0, svgOrigin: "280 100" }, { y: -40, rotation: 18, svgOrigin: "280 100", duration: 0.45, ease: "back.out(2)" }, 594.9);
tl.fromTo("#g30", { opacity: 0, scale: 0.3, y: 60, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2)", immediateRender: false }, 595.0);
tl.fromTo("#g30", { scale: 1 }, { scale: 1.18, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, 602.84);''')
SFX += [(590.55, "whoosh-3", 0.3, "gift in"), (591.62, "43-click-tonal", 0.26, "link"), (594.9, "24-ding-ring", 0.26, "30 days"), (602.84, "30-blip-pop", 0.26, "30 again"), (603.35, "whoosh-2", 0.2, "gift out")]

# 19) white label 666.6 -> 676.4
panel("wl", 666.6, 676.4, '''<span class="label">Software as a service</span><span class="headline">Your brand <em>on top</em></span>
<div class="wlstack"><div class="wlc back" id="wl1"><b>HighLevel</b><span>on the back end</span></div><div class="wlc front" id="wl2"><b>YOUR BRAND</b><span>CRM software</span></div></div>
<div class="chips"><span class="chip" id="wl3">Sold to business owners</span></div>''')
J.append('popIn("#wl1", 667.56); tl.fromTo("#wl2", { x: 260, opacity: 0, rotation: 6 }, { x: 0, opacity: 1, rotation: -3, duration: 0.5, ease: "back.out(1.6)" }, 670.53); popIn("#wl3", 674.15);')
SFX += [(666.55, "whoosh-4", 0.3, "wl in"), (667.56, POP(), 0.28, "HL card"), (670.48, "whoosh-1", 0.26, "brand slides"), (674.15, POP(), 0.28, "sold"), (675.95, "whoosh-2", 0.2, "wl out")]

# 20) recap 730.8 -> 741.2
rec = ["GHL VA for hire", "Onboarding support", "Social media VA", "Automation builder", "Success manager", "HighLevel affiliate", "Your own SaaS"]
h, js = items("recap", rec, [round(731.4 + k * 0.45, 2) for k in range(7)])
panel("recap", 730.8, 741.2, f'<span class="label">7 ways to earn with GHL</span>{h}{meter(7, "m wide")}', head=False)
J += js
SFX += [(730.75, "whoosh-3", 0.3, "recap in"), (734.7, "24-ding-ring", 0.24, "recap done"), (740.75, "whoosh-2", 0.2, "recap out")]

# 21) Chad AI 742.8 -> 762.6 (illustrated)
SC.stage(H, J, SFX, "cai", 742.8, 762.6, "Chad AI Community &middot; launching soon", [
    ("learnai", "Learn AI", 745.22, None), ("techva", "Technical VA", 747.52, None),
    ("gears", "Automation", 751.29, None), ("hlplat", "HighLevel", 752.79, None)],
    tail_html='<div class="chips"><span class="chip" id="cai-b">Technical VA bootcamp</span></div>',
    tail_js=['popIn("#cai-b", 755.9);'])
SFX += [(755.9, "24-ding-ring", 0.22, "bootcamp")]
PANELS.append((742.8, 762.6))

# 22) tools logos 797.3 -> 801.4
H.append('''<div id="ref-tools" class="clip ref" data-start="797.3" data-duration="4.1" data-track-index="16"><div class="card">
<div class="glow"></div><div class="logos"><img id="lg1" src="assets/refs/n8n.svg" alt="n8n" /><img id="lg2" src="assets/refs/zapier.svg" alt="Zapier" /></div>
<div class="tag"><span class="name">n8n + Zapier</span><span class="sub">Automation tools</span></div></div></div>''')
J.append('refCardLogos("#ref-tools", 797.3, 801.4, 797.62, 798.49);')
SFX += [(797.62, "30-blip-pop", 0.32, "n8n"), (798.49, "43-click-tonal", 0.32, "zapier")]

# ---------------------------------------------------------------- B-roll
BROLL = [  # id, file, in, out, enter, move, label
    ("smb", "small-business-owner.jpg", 86.5, 91.9, "slide-l", "push", "Business owners"),
    ("learn", "learning-on-the-job.jpg", 112.15, 115.4, "punch", "pull", "Learning on the job"),
    ("agency", "agency-meeting.jpg", 131.2, 135.7, "slide-r", "pan-r", "GHL agencies"),
    ("onboard", "onboarding-call.jpg", 144.0, 148.4, "split", "push", "Client onboarding"),
    ("dms", "social-messages.jpg", 209.8, 214.0, "slide-l", "pan-l", "Social DMs"),
    ("blueprint", "blueprint.jpg", 346.0, 350.4, "punch", "push", "System architect"),
    ("solo", "solo-business-owner.jpg", 389.0, 394.6, "slide-r", "pull", "Small teams"),
    ("clock", "clock-hours.jpg", 533.1, 537.0, "slide-l", "push", "8 hours isn't enough"),
    ("network", "networking.jpg", 539.0, 543.2, "split", "pan-r", "Business networking"),
    ("saas", "saas-dashboard.jpg", 677.1, 681.6, "punch", "push", "Your own SaaS"),
    ("watch", "watching-youtube.jpg", 720.6, 725.0, "slide-r", "pull", "Business owners"),
]
SHOTS = [  # id, file, in, out, box, zoom, fact, credit
    ("lastsep", "last-september.jpg", 36.1, 40.45, [33, 44, 44, 44], 1.25, '<b>Last September</b>', "Chad's photo"),
    ("proof", "ghl-proof.png", 40.15, 45.05, [36.5, 30, 33, 3.5], 1.8, 'GHL Proof: <b>HighLevel Certified Admin</b>', "Chad's certification email"),
    ("client", "ghl-client.jpg", 44.75, 49.75, [30, 30, 40, 40], 1.12, 'Now: <b>my GHL client</b>', "Chad's client call"),
    ("optin", "optin-form.png", 273.4, 279.0, [5.4, 77, 45.3, 6.4], 1.6, 'A form that asks for the <b>email</b>', "Example: chadgodoy.io/checklist, Nov 6 2026"),
    ("caveat", "caveat-definition.png", 400.2, 405.4, [2.5, 58.5, 37.8, 7.5], 1.5, '<b>Caveat</b> = a warning', "Screenshot: Cambridge Dictionary, Nov 6 2026"),
    ("aff", "ghl-affiliate.png", 568.6, 574.3, [26.3, 79.5, 22.4, 9.5], 1.8, 'HighLevel affiliates earn <b>40% lifetime</b> commissions', "Screenshot: gohighlevel.com/affiliateoffers, Nov 6 2026 (HighLevel's own figures)"),
    ("price", "ghl-pricing.png", 702.4, 708.4, [41.8, 24.5, 16.3, 11.4], 1.8, 'HighLevel Founder plan: <b>$497/month</b>, SaaS mode included', "Screenshot: gohighlevel.com/pricing, Nov 6 2026"),
    ("wait", "chad-ai-waitlist.png", 765.4, 771.6, [61.3, 60.3, 31.5, 6.8], 1.5, 'Join the <b>Chad AI</b> waitlist &middot; link below', "chadgodoy.io/chad-ai"),
]
BR_HTML = []
for bid, f, a, b, en, mv, lab in BROLL:
    img = f'<img class="img" src="assets/broll/{f}" alt="{lab}" />'
    inner = (f'<div class="half top">{img}</div><div class="half bot">{img}</div><div class="seam"></div>' if en == "split" else img)
    BR_HTML.append(f'<div id="br-{bid}" class="clip broll" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="12"><div class="frame">{inner}<div class="shade"></div><span class="label">{lab}</span><span class="credit">Photo: Unsplash</span></div></div>')
    J.append(f'brollCut("#br-{bid}", {a}, {b}, {{ enter: "{en}", move: "{mv}", label: true }});')
    if en.startswith("slide"): SFX += [(round(a - 0.05, 2), "whoosh-4", 0.25, "broll in"), (round(b - 0.4, 2), "whoosh-2", 0.18, "broll out")]
    else: SFX += [(a, "50-thump-short", 0.28, "broll punch/split")]
for sid, f, a, b, box, z, fact, credit in SHOTS:
    l, t, w, hh = box
    hlon = sid not in ("lastsep", "client")
    hlhtml = f'<div class="hl" style="left: {l}%; top: {t}%; width: {w}%; height: {hh}%"></div>' if hlon else ""
    BR_HTML.append(f'<div id="br-{sid}" class="clip broll" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{14 if sid == 'proof' else 12}"><div class="frame paper"><span class="fact">{fact}</span><div class="shot"><div class="zoom"><img src="assets/broll/{f}" alt="" />{hlhtml}</div></div><span class="credit">{credit}</span></div></div>')
    J.append(f'brollShot("#br-{sid}", {a}, {b}, {{ box: {box}, zoom: {z}, hl: {str(hlon).lower()}, fact: true }});')
    SFX += [(round(a - 0.05, 2), "whoosh-3", 0.25, "shot in"), (round(a + 2.3, 2), "30-blip-pop", 0.24, "highlighter"), (round(b - 0.35, 2), "whoosh-2", 0.18, "shot out")]

# ---------------------------------------------------------------- sketch boards
BOARDS = []
def board(bid, a, b, inks, paths, js):
    grain = f'<svg class="grain" width="1180" height="1080"><filter id="{bid}-grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="{len(BOARDS)+5}" /><feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.53  0 0 0 0 0.5  0 0 0 0.35 0" /></filter><rect width="1180" height="1080" filter="url(#{bid}-grain)" /></svg>'
    ink = "".join(f'<span class="ink{" hd" if hd else ""}" id="{bid}-{iid}" style="left: {x}px; top: {y}px; font-size: {fs}px;">{txt}</span>' for iid, txt, x, y, fs, hd in inks)
    pth = "".join(f'<path id="{bid}-{pid}" class="{c}" />' for pid, c in paths)
    H.append(f'<div id="{bid}" class="clip sketch" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="1"><div class="sheet"><div class="edge"></div><div class="paper">{grain}{ink}<svg class="draw" width="1180" height="1080">{pth}</svg></div></div></div>')
    J.append(f'tornEdge("#{bid} .paper", 1150, {len(BOARDS)+3}, 0); tornEdge("#{bid} .edge", 1150, {len(BOARDS)+3}, 7);')
    J.append(f'sketchIn("#{bid}", {a});')
    J.extend(js)
    J.append(f'sketchOut("#{bid}", {b});')
    BOARDS.append((a, b))
    SFX.extend([(round(a - 0.05, 2), "whoosh-3", 0.3, "board in"), (round(b - 0.45, 2), "whoosh-2", 0.2, "board out")])

DRAWS = []
def dr(sel, t, d):
    DRAWS.append((t, d))
    return f'draw("{sel}", {t}, {d});'

# Board 1 · snapshots 150.0 -> 165.6
board("skb1", 150.0, 165.6,
      [("t1", "Snapshot = template", 110, 100, 90, True), ("t2", "Template", 165, 372, 66, False),
       ("t3", "Client", 735, 342, 62, False), ("t4", "account", 735, 410, 62, False),
       ("t5", "manghula", 230, 610, 70, False), ("t6", "tamang setup", 230, 770, 76, False)],
      [("u1", "b"), ("r1", "n"), ("a1", "b"), ("a2", "b"), ("r2", "n"), ("x1", "b"), ("c1", "b")],
      ['setPath("skb1-u1", sk.line(110, 215, 830, 208, 31));',
       'setPath("skb1-r1", sk.rect(120, 330, 330, 170, 32));',
       'setPath("skb1-a1", sk.arrowShaft([[470, 415], [560, 405], [640, 415]], 33));',
       'setPath("skb1-a2", sk.arrowHead(640, 415, 0, 34));',
       'setPath("skb1-r2", sk.rect(680, 315, 380, 200, 35));',
       'setPath("skb1-x1", sk.cross(170, 655, 30, 36));',
       'setPath("skb1-c1", sk.check(140, 815, 64, 37));',
       'write("#skb1-t1", 150.6, 17);', dr("#skb1-u1", 152.4, 0.5),
       dr("#skb1-r1", 157.24, 0.7), 'write("#skb1-t2", 158.07, 16);',
       dr("#skb1-a1", 159.3, 0.4), dr("#skb1-a2", 159.7, 0.2),
       dr("#skb1-r2", 159.95, 0.7), 'write("#skb1-t3", 160.4, 16); write("#skb1-t4", 160.8, 16);',
       'write("#skb1-t5", 161.9, 18);', dr("#skb1-x1", 162.5, 0.35),
       'write("#skb1-t6", 162.9, 18);', dr("#skb1-c1", 163.7, 0.35)])

# Board 2 · dominoes 307.4 -> 325.4
dom_js = []
for k in range(6):
    x = 160 + k * 140
    dom_js.append(f'setPath("skb2-d{k}", sk.rect({x}, 360, 62, 230, {40+k}));')
board("skb2", 307.4, 325.4,
      [("t1", "Automation = dominoes", 110, 100, 90, True), ("t2", "TRIGGER", 105, 640, 70, False),
       ("t3", "the rest fall on their own", 330, 800, 72, False)],
      [("u1", "b")] + [(f"d{k}", "n") for k in range(6)] + [("p1", "b"), ("p2", "b"), ("c1", "b"), ("a1", "b"), ("a2", "b")],
      ['setPath("skb2-u1", sk.line(110, 215, 900, 208, 39));'] + dom_js +
      ['setPath("skb2-p1", sk.arrowShaft([[30, 300], [80, 380], [140, 470]], 47));',
       'setPath("skb2-p2", sk.arrowHead(140, 470, 1.0, 48));',
       'setPath("skb2-c1", sk.ellipse(191, 475, 85, 160, 49));',
       'setPath("skb2-a1", sk.arrowShaft([[240, 330], [560, 270], [900, 330]], 50));',
       'setPath("skb2-a2", sk.arrowHead(900, 330, 0.35, 51));',
       'write("#skb2-t1", 308.0, 17);', dr("#skb2-u1", 310.0, 0.5)] +
      [dr(f"#skb2-d{k}", round(311.4 + k * 0.5, 2), 0.4) for k in range(6)] +
      [dr("#skb2-p1", 314.94, 0.35), dr("#skb2-p2", 315.3, 0.2),
       dr("#skb2-c1", 316.9, 0.6), 'write("#skb2-t2", 318.14, 16);',
       'write("#skb2-t3", 319.68, 18);', dr("#skb2-a1", 320.4, 0.6), dr("#skb2-a2", 321.0, 0.2),
      ] + [f'tl.fromTo("#skb2-d{k}", {{ rotation: 0, svgOrigin: "{160+k*140+62} 590" }}, {{ rotation: 24, svgOrigin: "{160+k*140+62} 590", duration: 0.22, ease: "power2.in", immediateRender: false }}, {round(321.4+k*0.12,2)});' for k in range(6)])

# Board 3 · affiliate math 615.6 -> 647.4
board("skb3", 615.6, 647.4,
      [("t1", "Affiliate math", 110, 100, 90, True), ("t2", "40%", 130, 255, 120, False), ("t3", "&times; $97", 400, 255, 120, False),
       ("t4", "= $38.80 / month", 130, 430, 100, False), ("t5", "every month", 470, 650, 80, False), ("t6", "for years = $$$", 130, 820, 90, False)],
      [("u1", "b"), ("c1", "b"), ("l1", "b"), ("s1", "b")],
      ['setPath("skb3-u1", sk.line(110, 215, 640, 208, 61));',
       'setPath("skb3-c1", sk.ellipse(400, 495, 230, 78, 62));',
       'setPath("skb3-l1", sk.loop(300, 700, 130, 80, 63));',
       'setPath("skb3-s1", sk.star(860, 870, 64));',
       'write("#skb3-t1", 616.1, 17);', dr("#skb3-u1", 617.0, 0.45),
       'write("#skb3-t2", 618.03, 12);', 'write("#skb3-t3", 620.52, 12);',
       'write("#skb3-t4", 623.6, 16);', dr("#skb3-c1", 625.6, 0.7),
       dr("#skb3-l1", 635.84, 0.9), 'write("#skb3-t5", 636.4, 16);',
       'write("#skb3-t6", 644.49, 16);', dr("#skb3-s1", 645.6, 0.7)])
for i, (t, d) in enumerate(DRAWS):
    SFX.append((t, "pencil" if i % 2 == 0 else "pencil-rev", 0.15, "pencil (drawing)"))

# ---------------------------------------------------------------- end card
H.append(f'''<div id="endcard" class="clip" data-start="{FOOT}" data-duration="{round(ROOT-FOOT,2)}" data-track-index="8">
<div class="bg" id="end-bg"></div><div class="circle1" id="end-c1"></div><div class="circle2" id="end-c2"></div><div class="oring" id="end-ring"></div>
<div class="stack"><span class="thanks"><span class="w"><span class="ew">Salamat</span></span> <span class="w"><span class="ew">po!</span></span></span>
<div class="cag"><span id="cag1">CREATE</span><i id="cagd1"></i><span id="cag2">AUTOMATE</span><i id="cagd2"></i><span id="cag3">GROW</span></div>
<span class="word" id="end-word">Chad <em>Godoy</em></span><span class="site" id="end-site">chadgodoy.io<i class="ul" id="end-ul"></i></span></div></div>''')
E = FOOT
J.append(f'''tl.fromTo("#end-bg", {{ clipPath: "circle(0% at 55% 40%)" }}, {{ clipPath: "circle(150% at 55% 40%)", duration: 0.7, ease: "power2.inOut" }}, {E});
tl.fromTo(["#end-c1", "#end-c2"], {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease, stagger: 0.1 }}, {E+0.2});
tl.fromTo("#end-ring", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 1.4, ease }}, {E+0.3});
tl.fromTo("#endcard .ew", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.5, ease, stagger: 0.12 }}, {E+0.4});
[["#cag1", {E+1.0}], ["#cagd1", {E+1.2}], ["#cag2", {E+1.3}], ["#cagd2", {E+1.5}], ["#cag3", {E+1.6}]].forEach(([s, t]) => tl.fromTo(s, {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, t));
tl.fromTo("#end-word", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease }}, {E+1.9});
tl.fromTo("#end-site", {{ y: 18, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease }}, {E+2.1});
tl.fromTo("#end-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease }}, {E+2.35});''')
SFX += [(round(E - 0.05, 2), "whoosh-7", 0.45, "end wipe"), (round(E + 0.4, 2), "whoosh-1", 0.22, "thanks"),
        (round(E + 1.0, 2), "impact", 0.28, "slam 1"), (round(E + 1.3, 2), "impact", 0.28, "slam 2"), (round(E + 1.6, 2), "impact", 0.28, "slam 3"),
        (round(E + 1.9, 2), "55-orchestra-hit-sparkle", 0.22, "wordmark")]

# panel in/out whooshes are added per panel above; nothing else.

# ---------------------------------------------------------------- camera track
EV.sort()
for (a1, e1, _), (a2, _, _) in zip(EV, EV[1:]):
    assert e1 <= a2 + 1e-6, f"camera overlap {a1}-{e1} vs {a2}"
CAM, cursor, flip = [], 0.0, [0]
def fill(a, b):
    gap = b - a
    if gap < 4: return
    cycles = max(1, round(gap / 16)); seg = gap / cycles
    for k in range(cycles):
        s0 = a + k * seg; half = (seg - 0.2) / 2
        peak = (1.06, 1.07, 1.05)[flip[0] % 3]; flip[0] += 1
        CAM.append((round(s0 + 0.1, 2), peak, round(half, 2), "sine.inOut"))
        CAM.append((round(s0 + 0.1 + half, 2), 1, round(half, 2), "sine.inOut"))
for a, e, kfs in EV:
    fill(cursor, a); CAM.extend(kfs); cursor = e
fill(cursor, FOOT - 0.5)

# ---------------------------------------------------------------- audio tags
DUR = {"whoosh-1": 0.45, "whoosh-2": 0.23, "whoosh-3": 0.43, "whoosh-4": 0.39, "whoosh-5": 0.37, "whoosh-7": 0.67,
       "tick": 0.06, "pop": 0.15, "ding": 1.1, "impact": 0.6, "pencil": 1.422, "pencil-rev": 1.422}
cat = json.load(open(f"{LIB}/catalog.json"))
BANNED = {c["file"][:-4] for c in cat if c.get("banned")} | {"heartbeat"}
for c in cat: DUR[c["file"][:-4]] = c["duration"]
PL = {t: d for t, d in DRAWS}
SFX_DIR = os.path.join(os.path.dirname(os.path.abspath(OUT)), "assets/sfx")
POOL = [9, 10, 11, 13, 14] + list(range(18, 39))
last = {tr: -1 for tr in POOL}
AUD = []
_seen = set(); SFX = [x for x in sorted(SFX) if not ((x[0], x[1]) in _seen or _seen.add((x[0], x[1])))]
for n, (t, s, v, note) in enumerate(SFX, 1):
    assert s not in BANNED, s
    if s[:2].isdigit() and not os.path.exists(f"{SFX_DIR}/{s}.wav"):
        shutil.copy(f"{LIB}/{s}.wav", f"{SFX_DIR}/{s}.wav")
    d = min(DUR[s], ROOT - t, (PL.get(t, 99) + 0.05) if s.startswith("pencil") else 99)
    tr = next(tr for tr in POOL if last[tr] <= t + 1e-6); last[tr] = t + d
    AUD.append(f'<audio id="sfx-{n:03d}" src="assets/sfx/{s}.wav" data-start="{t}" data-duration="{d:.3f}" data-volume="{v}" data-track-index="{tr}"></audio> <!-- {note} -->')

cues = json.load(open(CUES))
for c in cues: c["e"] = min(c["e"], SUB_END)
HIDE = [[a, b] for _, a, b, _, _ in CAPS]

EXTRA_CSS = SC.CSS + """
#cam { transform-origin: 1000px 420px; }
.slam .mrow { display: flex; align-items: flex-end; justify-content: space-between; margin-top: 16px; }
.slam .mlab, .psub { font-weight: 700; font-size: 16px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--pale); }
.psub { display: block; margin-top: 14px; font-size: 17px; }
.psub b { color: var(--gold); }
.meter { display: flex; align-items: flex-end; gap: 6px; }
.meter i { display: block; width: 18px; border-radius: 4px; background: rgba(56, 130, 246, 0.25); transform-origin: 50% 100%; }
.meter i.on { background: var(--light); }
.meter i.now { background: var(--gold); }
.meter.wide { margin-top: 12px; justify-content: center; }
.meter.wide i { width: 34px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.chip { display: inline-block; background: rgba(37, 99, 235, 0.25); border: 2px solid var(--light); border-radius: 999px; padding: 6px 14px; font-weight: 700; font-size: 17px; white-space: nowrap; }
.chip.tag { background: var(--gold); border-color: var(--gold); color: var(--navy); }
.price { display: flex; align-items: baseline; gap: 10px; margin-top: 8px; position: relative; }
.price b { display: inline-block; white-space: nowrap; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 74px; line-height: 1; }
.price span { white-space: nowrap; font-family: "Poppins", Arial, sans-serif; font-weight: 700; font-size: 22px; color: var(--light); }
.price.old b { font-size: 54px; color: rgba(234, 243, 255, 0.6); }
.price.old span { font-size: 20px; }
.pstrike { position: absolute; left: -4px; width: 190px; top: 50%; height: 6px; border-radius: 3px; background: var(--red); transform-origin: left; }
.stampin { display: inline-block; margin-top: 18px; padding: 8px 16px; border: 5px solid var(--gold); border-radius: 12px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 30px; color: var(--gold); text-transform: uppercase; }
.tline { position: relative; margin-top: 18px; padding-left: 34px; display: flex; flex-direction: column; gap: 18px; }
.tl-rail { position: absolute; left: 10px; top: 10px; bottom: 10px; width: 5px; border-radius: 3px; background: var(--light); transform-origin: top; }
.tnode { position: relative; }
.tnode::before { content: ""; position: absolute; left: -32px; top: 6px; width: 18px; height: 18px; border-radius: 50%; background: var(--gold); border: 3px solid var(--navy); }
.tnode b { display: block; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 26px; color: var(--light); }
.tnode span { display: block; font-weight: 700; font-size: 21px; }
.flow { margin-top: 14px; display: flex; flex-direction: column; align-items: stretch; }
.fnode { display: flex; align-items: center; gap: 12px; border-radius: 14px; padding: 9px 14px; background: rgba(37, 99, 235, 0.16); border: 2px solid rgba(56, 130, 246, 0.5); }
.fnode.on { background: var(--blue); border-color: var(--pale); }
.fk { font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 17px; letter-spacing: 0.08em; color: var(--gold); min-width: 96px; }
.ft { font-weight: 700; font-size: 19px; white-space: nowrap; }
.farrow { display: block; width: 4px; height: 14px; margin: 3px auto; background: var(--light); }
.days { display: flex; gap: 8px; margin: 16px 0 14px; }
.day { position: relative; flex: 1; height: 86px; border-radius: 12px; background: rgba(37, 99, 235, 0.2); border: 2px solid rgba(56, 130, 246, 0.5); display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 8px 0; }
.day span { font-weight: 700; font-size: 14px; letter-spacing: 0.1em; color: var(--pale); }
.day i { font-style: normal; font-weight: 800; font-size: 30px; color: #22c55e; }
.wlstack { position: relative; height: 210px; margin-top: 16px; }
.wlc { position: absolute; width: 300px; height: 150px; border-radius: 18px; display: flex; flex-direction: column; justify-content: center; padding: 0 24px; }
.wlc b { font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 34px; }
.wlc span { font-weight: 700; font-size: 16px; letter-spacing: 0.12em; text-transform: uppercase; }
.wlc.back { left: 0; top: 0; background: #1e3a8a; border: 2px solid var(--light); color: var(--pale); }
.wlc.front { left: 70px; top: 54px; background: var(--gold); color: var(--navy); box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35); }
.ref .img.portrait { width: 320px; height: 376px; object-fit: cover; border-radius: 20px; border: 6px solid #ffffff; }
.ref .img.portrait.sm { width: 230px; height: 270px; }
.ref .img.icon { position: relative; width: 230px; height: 230px; }
.ref .tag.t2 { margin-top: 10px; background: var(--blue); }
.ref .name.sm { font-size: 24px; }
.ref .glow { top: 40px; }
"""
REF_JS = """
      function refCard(id, inAt, outAt) {
        tl.fromTo(id + " .glow", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power2.out" }, inAt);
        tl.fromTo(id + " .img", { scale: 0.3, opacity: 0, rotation: -8, y: 40 }, { scale: 1, opacity: 1, rotation: 0, y: 0, duration: 0.55, ease: "back.out(2)" }, inAt);
        tl.fromTo(id + " .img", { y: 0 }, { y: -10, duration: (outAt - inAt - 0.9) / 2, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, inAt + 0.55);
        tl.fromTo(id + " .tag", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, inAt + 0.25);
        tl.to(id + " .card", { scale: 0.85, opacity: 0, duration: 0.3, ease: "power2.in" }, outAt - 0.3);
      }
      function refCardLogos(id, inAt, outAt, t1, t2) {
        tl.fromTo(id + " .glow", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power2.out" }, inAt);
        tl.fromTo(id + " #lg1", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, t1);
        tl.fromTo(id + " #lg2", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, t2);
        tl.fromTo(id + " .tag", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, inAt + 0.25);
        tl.to(id + " .card", { scale: 0.85, opacity: 0, duration: 0.3, ease: "power2.in" }, outAt - 0.3);
      }
      function slam7(id, inAt, outAt) {
        panelIn(id, inAt);
        tl.fromTo(id + " .big b", { scale: 2.2, opacity: 0, transformOrigin: "0% 80%" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, inAt + 0.05);
        tl.fromTo(id + " .big span", { x: -20, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease }, inAt + 0.3);
        tl.fromTo(id + " .meter i", { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.07 }, inAt + 0.55);
        tl.fromTo(id + " .meter i.now", { scaleX: 1 }, { scaleX: 1.3, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, inAt + 1.2);
        tl.fromTo(id + " .psub", { y: 12, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease }, inAt + 0.9);
        panelOut(id, outAt);
      }
"""
SUBS_JS = f"""
      const SUB_CUES = {json.dumps(cues, ensure_ascii=False)};
      const SUB_HIDE = {json.dumps(HIDE)};
      const subEl = document.getElementById("sub-text");
      const subProxy = {{ t: 0 }};
      let subLast = null;
      tl.fromTo(subProxy, {{ t: 0 }}, {{
        t: {SUB_END}, duration: {SUB_END}, ease: "none",
        onUpdate: () => {{
          const t = subProxy.t;
          let cue = null;
          if (!SUB_HIDE.some(([a, b]) => t >= a && t < b)) cue = SUB_CUES.find(c => t >= c.s && t < c.e) || null;
          if (cue !== subLast) {{ subLast = cue; subEl.textContent = cue ? cue.t : ""; subEl.style.opacity = cue ? 1 : 0; }}
        }}
      }}, 0);"""

helpers = HELPERS.replace("__CAM__", json.dumps([[t, s, d, e] for t, s, d, e in CAM]))
html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}
{BR_CSS}
{EXTRA_CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{ROOT}" data-width="1920" data-height="1080">
      <div id="cam">
        <video id="a-roll" class="clip" src="footage_cut2.mp4" playsinline data-start="0" data-duration="{FOOT}" data-track-index="0"
          style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover" data-has-audio="true"></video>
      </div>
{chr(10).join(BR_HTML)}
      <audio id="music-bed" src="assets/music/bed.wav" data-start="0" data-duration="{ROOT}" data-volume="0.4365" data-track-index="40"></audio>
{chr(10).join(AUD)}
      <div id="subs" class="clip" data-start="0" data-duration="{SUB_END}" data-track-index="15"><div class="sub-wrap"><span class="sub" id="sub-text"></span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="{SUB_END}" data-track-index="6"><div class="track"></div><div class="fill" id="progress-fill"></div></div>
      <div id="swipe" class="clip" data-start="0" data-duration="1.2" data-track-index="5"><div class="sb sb3" id="sb3"></div><div class="sb sb2" id="sb2"></div><div class="sb sb1" id="sb1"></div></div>
{chr(10).join(H)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const ease = "power3.out";
      const SVGNS = "http://www.w3.org/2000/svg";
{helpers}
{REF_JS}
{BR_JS}
      tl.fromTo("#progress-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {SUB_END}, ease: "none" }}, 0);
      tl.fromTo(["#sb1", "#sb2", "#sb3"], {{ x: 0, skewX: -18 }}, {{ x: 3200, skewX: -18, duration: 1.0, ease: "power2.inOut", stagger: 0.06 }}, 0);
      {chr(10).join("      " + l for l in J)}
{SUBS_JS}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(OUT, "w").write(html)
# overlap report for right-side zone (panels, slams, refs, boards, brolls)
zone = sorted([(a, b, "panel") for a, b in PANELS] + [(a, b, "slam") for _, a, b, _, _ in PATHS] + [(a, b, "board") for a, b in BOARDS] +
              [(a, b, "broll " + i) for i, _, a, b, *_ in BROLL] + [(a, b, "shot " + i) for i, _, a, b, *_ in SHOTS] +
              [(422.2, 428.4, "hla"), (465.5, 472.4, "liz"), (548.8, 554.4, "liz2"), (797.3, 801.4, "tools"), (395.4, 399.9, "stamp")])
for (a1, b1, n1), (a2, b2, n2) in zip(zone, zone[1:]):
    if a2 < b1 - 0.01: print(f"!! overlap {n1} {a1}-{b1} with {n2} {a2}-{b2}")
print(f"{len(AUD)} sfx, {len(cues)} cues, {len(CAM)} cam keyframes, {len(EV)} moves, max track {max(t for t in last if last[t] > 0)}")
