"""Motion-graphic scenes for the 7 Ways v2 edit (The creator's notes 2026-11-06):
HighLevel-logo hub, full-screen kinetic text, full-screen path scenes, and illustrated "stages"
that replace enumerated lists. All SVG is built here; animations are GSAP lines for the main tl.
Each illustration is drawn in a 440x320 viewBox. ill(key, p, t, extra) -> (svg, js, sfx)
"""
import math

NAVY, BLUE, LIGHT, PALE, GOLD = "#0B2058", "#2563EB", "#3882F6", "#EAF3FF", "#FFC531"
GREEN, RED = "#22C55E", "#EF4444"
E = "power3.out"


def pop(sel, t, d=0.4, s0=0.3):
    return f'tl.fromTo("{sel}", {{ scale: {s0}, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: {d}, ease: "back.out(2)" }}, {t:.2f});'


def slide(sel, t, x=0, y=0, d=0.45):
    return f'tl.fromTo("{sel}", {{ x: {x}, y: {y}, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: {d}, ease: "{E}" }}, {t:.2f});'


def grow(sel, t, d=0.5, origin="0 0"):
    return f'tl.fromTo("{sel}", {{ scaleX: 0, svgOrigin: "{origin}" }}, {{ scaleX: 1, svgOrigin: "{origin}", duration: {d}, ease: "power2.out" }}, {t:.2f});'


def drawp(sel, t, d=0.6):
    return f'tl.fromTo("{sel}", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power1.inOut" }}, {t:.2f});'


def gear_path(cx, cy, r, teeth=8, depth=None):
    depth = depth or r * 0.22
    pts = []
    n = teeth * 4
    for i in range(n):
        a = i / n * math.tau
        rr = r + depth if (i % 4) in (1, 2) else r
        pts.append(f"{cx + math.cos(a) * rr:.1f},{cy + math.sin(a) * rr:.1f}")
    return "M" + " L".join(pts) + " Z"


def calendar_svg(p, checks=True):
    cells, cks = "", ""
    k = 0
    for r in range(3):
        for c in range(5):
            x, y = 62 + c * 66, 104 + r * 58
            cells += f'<rect x="{x}" y="{y}" width="56" height="48" rx="8" fill="{PALE}"/>'
            if checks and (r * 5 + c) in (0, 2, 4, 6, 8, 11, 13):
                cks += f'<path id="{p}-c{k}" d="M{x+14} {y+25} L{x+24} {y+35} L{x+43} {y+13}" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
                k += 1
    svg = (f'<rect x="40" y="26" width="360" height="282" rx="20" fill="#ffffff"/>'
           f'<rect x="40" y="26" width="360" height="62" rx="20" fill="{BLUE}"/><rect x="40" y="66" width="360" height="22" fill="{BLUE}"/>'
           f'<text x="220" y="66" font-size="24" fill="#fff" text-anchor="middle" font-family="Poppins">THIS WEEK</text>'
           f'<circle cx="96" cy="26" r="9" fill="{NAVY}"/><circle cx="344" cy="26" r="9" fill="{NAVY}"/>{cells}{cks}')
    return svg, k


def ill(key, p, t, extra=None):
    """Return (svg_inner, js_lines, sfx) for illustration `key`, ids prefixed with p, starting at t."""
    js, sfx = [], []
    if key == "contacts":
        rows = ""
        cols = [BLUE, GOLD, GREEN, LIGHT]
        for k in range(4):
            y = 84 + k * 54
            rows += (f'<g id="{p}-r{k}"><circle cx="82" cy="{y+20}" r="17" fill="{cols[k]}"/>'
                     f'<rect x="112" y="{y+8}" width="170" height="13" rx="6" fill="{NAVY}" opacity="0.85"/>'
                     f'<rect x="112" y="{y+28}" width="110" height="10" rx="5" fill="#94A3B8"/>'
                     f'<rect x="304" y="{y+11}" width="74" height="20" rx="10" fill="{LIGHT}"/></g>')
        svg = (f'<rect x="40" y="20" width="360" height="290" rx="20" fill="#ffffff"/>'
               f'<rect x="40" y="20" width="360" height="52" rx="20" fill="{BLUE}"/><rect x="40" y="52" width="360" height="20" fill="{BLUE}"/>'
               f'<text x="66" y="55" font-size="22" fill="#fff" font-family="Poppins">Contacts</text>'
               f'<rect id="{p}-hl" x="52" y="134" width="336" height="52" rx="12" fill="{GOLD}" opacity="0"/>{rows}'
               f'<g id="{p}-ck"><circle cx="372" cy="160" r="22" fill="{GREEN}"/><path d="M361 160 L369 168 L384 151" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>')
        js += [slide(f"#{p}-r{k}", t + 0.1 + k * 0.12, x=50) for k in range(4)]
        js += [f'tl.fromTo("#{p}-hl", {{ opacity: 0 }}, {{ opacity: 0.45, duration: 0.3 }}, {t+0.9:.2f});', pop(f"#{p}-ck", t + 1.1)]
        sfx += [(t + 1.1, "24-ding-ring", 0.2)]
    elif key == "mail":
        svg = (f'<path id="{p}-tr" d="M120 230 C 200 150, 260 290, 390 80" fill="none" stroke="{LIGHT}" stroke-width="5" stroke-dasharray="1" pathLength="1" stroke-linecap="round"/>'
               f'<g id="{p}-env"><rect x="40" y="190" width="120" height="82" rx="10" fill="{PALE}"/><path d="M40 196 L100 240 L160 196" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/></g>'
               f'<g id="{p}-pl"><polygon points="100,200 180,222 100,244 116,222" fill="{GOLD}"/><polygon points="116,222 180,222 122,238" fill="#E0A400"/></g>'
               f'<g id="{p}-ok"><rect x="290" y="250" width="130" height="44" rx="22" fill="{GREEN}"/><text x="355" y="280" font-size="22" fill="#fff" text-anchor="middle" font-family="Poppins">SENT</text></g>')
        js += [pop(f"#{p}-env", t), drawp(f"#{p}-tr", t + 0.35, 0.9),
               f'tl.fromTo("#{p}-pl", {{ x: 0, y: 0, rotation: 0, opacity: 0, svgOrigin: "140 222" }}, {{ keyframes: [{{ opacity: 1, duration: 0.05 }}, {{ x: 110, y: -40, rotation: -25, duration: 0.45, ease: "sine.inOut" }}, {{ x: 250, y: -150, rotation: -40, duration: 0.45, ease: "sine.in" }}], svgOrigin: "140 222" }}, {t+0.3:.2f});',
               pop(f"#{p}-ok", t + 1.3)]
        sfx += [(t + 0.3, "whoosh-1", 0.22), (t + 1.3, "43-click-tonal", 0.24)]
    elif key in ("calendar", "booking"):
        svg, k = calendar_svg(p, checks=(key == "calendar"))
        if key == "calendar":
            js += [f'tl.fromTo("#{p}-c{i}", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.2 }}, {t+0.3+i*0.14:.2f});' for i in range(k)]
            svg = svg.replace('stroke-linejoin="round"/>', 'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
            sfx += [(t + 0.3 + i * 0.14, "49-click-tiny", 0.2) for i in range(0, k, 2)]
        else:
            svg += (f'<g id="{p}-bk"><circle cx="220" cy="190" r="74" fill="{GREEN}" stroke="#fff" stroke-width="8"/>'
                    f'<path d="M185 190 L210 215 L258 164" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>'
                    f'<g id="{p}-tag"><rect x="140" y="276" width="160" height="40" rx="20" fill="{GOLD}"/><text x="220" y="303" font-size="20" fill="{NAVY}" text-anchor="middle" font-family="Poppins">BOOKED!</text></g>')
            js += [pop(f"#{p}-bk", t + 0.5, 0.45, 2.2), pop(f"#{p}-tag", t + 0.9)]
            sfx += [(t + 0.5, "06-impact-punch", 0.24)]
    elif key == "traits":
        t1, t2, t3 = extra
        teeth = gear_path(360, 130, 46, 8)
        svg = (f'<g id="{p}-a"><path d="M80 60 L130 80 L130 130 C130 165 105 185 80 195 C55 185 30 165 30 130 L30 80 Z" fill="{BLUE}" stroke="#fff" stroke-width="5"/>'
               f'<path d="M58 128 L75 145 L104 112" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<text x="80" y="250" font-size="24" fill="#fff" text-anchor="middle" font-family="Poppins">Reliable</text></g>'
               f'<g id="{p}-b"><rect x="168" y="78" width="104" height="80" rx="10" fill="{LIGHT}"/><rect x="176" y="96" width="104" height="80" rx="10" fill="{GOLD}"/>'
               f'<rect x="184" y="114" width="104" height="80" rx="10" fill="{PALE}"/><rect x="184" y="104" width="44" height="18" rx="6" fill="{PALE}"/>'
               f'<text x="228" y="250" font-size="24" fill="#fff" text-anchor="middle" font-family="Poppins">Organized</text></g>'
               f'<g id="{p}-c"><g id="{p}-g"><path d="{teeth}" fill="{PALE}"/><circle cx="360" cy="130" r="18" fill="{NAVY}"/></g>'
               f'<text x="360" y="250" font-size="24" fill="#fff" text-anchor="middle" font-family="Poppins">Techie</text></g>')
        js += [pop(f"#{p}-a", t1), pop(f"#{p}-b", t2), pop(f"#{p}-c", t3),
               f'tl.fromTo("#{p}-g", {{ rotation: 0, svgOrigin: "360 130" }}, {{ rotation: 240, svgOrigin: "360 130", duration: 3, ease: "none" }}, {t3:.2f});']
        sfx += [(t1, "30-blip-pop", 0.26), (t2, "43-click-tonal", 0.26), (t3, "60-blip-tonal", 0.26)]
    elif key == "bizinfo":
        svg = (f'<rect x="40" y="40" width="360" height="240" rx="20" fill="#ffffff"/>'
               f'<g id="{p}-st"><rect x="70" y="110" width="110" height="130" rx="8" fill="{BLUE}"/>'
               + "".join(f'<rect x="{70+i*22}" y="84" width="22" height="34" fill="{GOLD if i % 2 == 0 else "#ffffff"}" stroke="{NAVY}" stroke-width="2"/>' for i in range(5))
               + f'<rect x="108" y="180" width="34" height="60" rx="4" fill="{PALE}"/></g>'
               + "".join(f'<rect id="{p}-l{i}" x="206" y="{98+i*40}" width="{[160,120,140,100][i]}" height="16" rx="8" fill="{NAVY if i == 0 else "#94A3B8"}"/>' for i in range(4)))
        js += [pop(f"#{p}-st", t + 0.05)] + [grow(f"#{p}-l{i}", t + 0.35 + i * 0.15, 0.4, f"206 {106+i*40}") for i in range(4)]
    elif key == "branding":
        cols = [NAVY, BLUE, GOLD, LIGHT]
        svg = ("".join(f'<circle id="{p}-k{i}" cx="{100+i*80}" cy="96" r="34" fill="{c}" stroke="#fff" stroke-width="4"/>' for i, c in enumerate(cols))
               + f'<text id="{p}-aa" x="70" y="268" font-size="110" fill="#fff" font-family="Poppins">Aa</text>'
               + f'<g id="{p}-lg"><rect x="280" y="170" width="100" height="100" rx="18" fill="{GOLD}" transform="rotate(45 330 220)"/><text x="330" y="236" font-size="44" fill="{NAVY}" text-anchor="middle" font-family="Poppins">B</text></g>')
        js += [pop(f"#{p}-k{i}", t + i * 0.08) for i in range(4)] + [slide(f"#{p}-aa", t + 0.2, y=30), pop(f"#{p}-lg", t + 0.3)]
    elif key in ("socialacc", "platforms"):
        plats = [("f", "#1877F2"), ("ig", "#E1306C"), ("in", "#0A66C2"), ("tt", "#111111"), ("G", "#34A853")]
        if key == "socialacc":
            plats = plats[:4]
            pos = [(80, 70), (360, 70), (80, 250), (360, 250)]
            center = f'<g id="{p}-hub"><circle cx="220" cy="160" r="50" fill="{BLUE}" stroke="#fff" stroke-width="5"/><text x="220" y="170" font-size="28" fill="#fff" text-anchor="middle" font-family="Poppins">GHL</text></g>'
        else:
            pos = [(220 + math.cos(a) * 170, 175 + math.sin(a) * 125) for a in [math.pi * (1.0 + i * 0.25) for i in range(5)]]
            center = (f'<g id="{p}-hub"><rect x="160" y="150" width="120" height="110" rx="16" fill="#fff"/><rect x="160" y="150" width="120" height="32" rx="16" fill="{BLUE}"/>'
                      f'<rect x="160" y="168" width="120" height="14" fill="{BLUE}"/><text x="220" y="236" font-size="40" fill="{NAVY}" text-anchor="middle" font-family="Poppins">31</text></g>')
        lines = "".join(f'<path id="{p}-ln{i}" d="M{x:.0f} {y:.0f} L220 {175 if key == "platforms" else 160}" stroke="{LIGHT}" stroke-width="5" stroke-dasharray="1" pathLength="1" stroke-dashoffset="1"/>' for i, (x, y) in enumerate(pos))
        icons = "".join(f'<g id="{p}-i{i}"><circle cx="{x:.0f}" cy="{y:.0f}" r="36" fill="{c}" stroke="#fff" stroke-width="4"/><text x="{x:.0f}" y="{y+11:.0f}" font-size="30" fill="#fff" text-anchor="middle" font-family="Poppins">{l}</text></g>' for i, ((l, c), (x, y)) in enumerate(zip(plats, pos)))
        svg = lines + center + icons
        js += [pop(f"#{p}-hub", t)] + [pop(f"#{p}-i{i}", t + 0.15 + i * 0.15) for i in range(len(pos))] + [drawp(f"#{p}-ln{i}", t + 0.3 + i * 0.15, 0.35) for i in range(len(pos))]
        sfx += [(t + 0.15 + i * 0.15, "49-click-tiny", 0.22) for i in range(len(pos))]
    elif key == "apps":
        svg = (f'<path d="M0 200 C 40 200, 50 160, 80 160" fill="none" stroke="{PALE}" stroke-width="10" stroke-linecap="round"/>'
               f'<g id="{p}-sk"><rect x="250" y="96" width="150" height="128" rx="24" fill="{PALE}"/><rect x="258" y="128" width="36" height="14" rx="5" fill="{NAVY}"/><rect x="258" y="178" width="36" height="14" rx="5" fill="{NAVY}"/>'
               f'<text x="350" y="172" font-size="22" fill="{NAVY}" text-anchor="middle" font-family="Poppins">APPS</text></g>'
               f'<g id="{p}-pg"><rect x="80" y="120" width="110" height="80" rx="16" fill="{BLUE}" stroke="#fff" stroke-width="4"/><rect x="190" y="130" width="60" height="14" rx="5" fill="{GOLD}"/><rect x="190" y="176" width="60" height="14" rx="5" fill="{GOLD}"/>'
               f'<text x="135" y="168" font-size="22" fill="#fff" text-anchor="middle" font-family="Poppins">GHL</text></g>'
               f'<g id="{p}-zap"><path d="M232 70 L220 100 L240 100 L226 132" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="M232 250 L220 222 L240 222 L226 192" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>'
               f'<g id="{p}-ok"><rect x="140" y="266" width="160" height="44" rx="22" fill="{GREEN}"/><text x="220" y="296" font-size="21" fill="#fff" text-anchor="middle" font-family="Poppins">CONNECTED</text></g>')
        js += [pop(f"#{p}-sk", t), f'tl.fromTo("#{p}-pg", {{ x: -70, opacity: 0 }}, {{ x: 8, opacity: 1, duration: 0.55, ease: "power3.out" }}, {t+0.2:.2f});',
               pop(f"#{p}-zap", t + 0.75), pop(f"#{p}-ok", t + 1.0)]
        sfx += [(t + 0.75, "50-thump-short", 0.24)]
    elif key == "writeposts":
        svg = (f'<rect x="110" y="16" width="220" height="296" rx="18" fill="#fff"/><rect id="{p}-im" x="128" y="34" width="184" height="112" rx="10" fill="{LIGHT}"/>'
               f'<circle cx="270" cy="72" r="16" fill="{GOLD}"/><path d="M128 146 L180 96 L222 136 L250 112 L312 146 Z" fill="{BLUE}"/>'
               + "".join(f'<rect id="{p}-t{i}" x="128" y="{164+i*28}" width="{[184,150,170][i]}" height="14" rx="7" fill="{NAVY if i == 0 else "#94A3B8"}"/>' for i in range(3))
               + f'<path id="{p}-ht" d="M290 282 C 290 268, 270 266, 270 280 C 270 266, 250 268, 250 282 C 250 296, 270 304, 270 310 C 270 304, 290 296, 290 282 Z" fill="{RED}"/>')
        js += [pop(f"#{p}-im", t, 0.4, 0.6)] + [grow(f"#{p}-t{i}", t + 0.25 + i * 0.18, 0.35, f"128 {171+i*28}") for i in range(3)] + [pop(f"#{p}-ht", t + 0.85, 0.35, 0.1)]
    elif key == "schedule":
        cal, _ = calendar_svg(p, checks=False)
        svg = (cal + f'<g id="{p}-ck"><circle cx="330" cy="236" r="70" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
               f'<line id="{p}-hh" x1="330" y1="236" x2="330" y2="196" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
               f'<line id="{p}-mh" x1="330" y1="236" x2="368" y2="236" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/><circle cx="330" cy="236" r="7" fill="{GOLD}"/></g>'
               f'<g id="{p}-ch"><rect x="60" y="250" width="170" height="44" rx="22" fill="{GOLD}"/><text x="145" y="280" font-size="21" fill="{NAVY}" text-anchor="middle" font-family="Poppins">MON 9:00 AM</text></g>')
        js += [pop(f"#{p}-ck", t + 0.1), f'tl.fromTo("#{p}-mh", {{ rotation: 0, svgOrigin: "330 236" }}, {{ rotation: 360, svgOrigin: "330 236", duration: 1.2, ease: "power1.inOut" }}, {t+0.2:.2f});', pop(f"#{p}-ch", t + 0.5)]
    elif key == "create":
        svg = (f'<g id="{p}-cam"><rect x="80" y="96" width="280" height="180" rx="26" fill="{BLUE}" stroke="#fff" stroke-width="5"/><rect x="160" y="72" width="90" height="34" rx="10" fill="{BLUE}" stroke="#fff" stroke-width="5"/>'
               f'<circle cx="220" cy="186" r="62" fill="{NAVY}" stroke="#fff" stroke-width="6"/><circle cx="220" cy="186" r="30" fill="{LIGHT}"/><circle cx="208" cy="174" r="9" fill="#fff"/></g>'
               f'<g id="{p}-rec"><circle cx="320" cy="124" r="10" fill="{RED}"/></g>'
               + "".join(f'<path id="{p}-s{i}" d="M{x} {y-18} L{x+5} {y-5} L{x+18} {y} L{x+5} {y+5} L{x} {y+18} L{x-5} {y+5} L{x-18} {y} L{x-5} {y-5} Z" fill="{GOLD}"/>' for i, (x, y) in enumerate([(56, 70), (396, 250), (380, 60)])))
        js += [pop(f"#{p}-cam", t, 0.45, 0.5)] + [pop(f"#{p}-s{i}", t + 0.4 + i * 0.15, 0.35, 0) for i in range(3)] + \
              [f'tl.fromTo("#{p}-rec", {{ opacity: 1 }}, {{ opacity: 0.1, duration: 0.3, yoyo: true, repeat: 3, ease: "none", immediateRender: false }}, {t+0.6:.2f});']
    elif key == "leads":
        ppl = ""
        for i in range(6):
            x, y = 300 + (i % 2) * 70, 70 + i * 36
            ppl += f'<g id="{p}-p{i}"><circle cx="{x}" cy="{y}" r="13" fill="{PALE}"/><path d="M{x-17} {y+34} C {x-17} {y+14}, {x+17} {y+14}, {x+17} {y+34} Z" fill="{PALE}"/></g>'
        svg = (f'<g id="{p}-mg"><path d="M60 90 L130 90 L130 130 L100 130 C 92 130 90 138 90 160 C 90 182 92 190 100 190 L130 190 L130 230 L60 230 C 30 230 20 200 20 160 C 20 120 30 90 60 90 Z" fill="{RED}"/>'
               f'<rect x="110" y="90" width="22" height="40" fill="#E2E8F0"/><rect x="110" y="190" width="22" height="40" fill="#E2E8F0"/></g>'
               + "".join(f'<path id="{p}-w{i}" d="M150 {130+i*30} q 12 -10 24 0 t 24 0" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>' for i in range(3)) + ppl)
        js += [pop(f"#{p}-mg", t)] + [f'tl.fromTo("#{p}-w{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, yoyo: true, repeat: 3, ease: "none" }}, {t+0.2+i*0.1:.2f});' for i in range(3)]
        js += [f'tl.fromTo("#{p}-p{i}", {{ opacity: 0, x: 40 }}, {{ keyframes: [{{ opacity: 1, x: 0, duration: 0.25 }}, {{ x: {-120 - (i % 2) * 70}, y: {160 - (70 + i * 36) - 10}, scale: 0.7, duration: 0.6, ease: "power2.in" }}], transformOrigin: "50% 50%" }}, {t+0.3+i*0.12:.2f});' for i in range(6)]
        sfx += [(t + 0.9, "43-click-tonal", 0.22)]
    elif key == "followup":
        bub = ""
        for i, (txt, alt) in enumerate([("Hi! Still interested?", False), ("Yes po!", True), ("Here's your link", False)]):
            y = 56 + i * 74
            if alt:
                bub += f'<g id="{p}-b{i}"><rect x="210" y="{y}" width="110" height="50" rx="16" fill="{BLUE}"/><text x="265" y="{y+32}" font-size="17" fill="#fff" text-anchor="middle" font-family="Montserrat">{txt}</text></g>'
            else:
                bub += f'<g id="{p}-b{i}"><rect x="130" y="{y}" width="180" height="50" rx="16" fill="{PALE}"/><text x="220" y="{y+32}" font-size="16" fill="{NAVY}" text-anchor="middle" font-family="Montserrat">{txt}</text></g>'
        svg = f'<rect x="112" y="8" width="216" height="304" rx="30" fill="{NAVY}" stroke="{PALE}" stroke-width="6"/><rect x="190" y="18" width="60" height="10" rx="5" fill="{PALE}"/>{bub}' + \
              "".join(f'<circle id="{p}-d{i}" cx="{150+i*20}" cy="286" r="6" fill="{PALE}"/>' for i in range(3))
        js += [pop(f"#{p}-b{i}", t + 0.1 + i * 0.4) for i in range(3)] + \
              [f'tl.fromTo("#{p}-d{i}", {{ y: 0 }}, {{ y: -8, duration: 0.18, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {t+0.1+i*0.08:.2f});' for i in range(3)]
        sfx += [(t + 0.1 + i * 0.4, ["30-blip-pop", "43-click-tonal", "60-blip-tonal"][i], 0.22) for i in range(3)]
    elif key == "learnai":
        nodes = [(80, 60), (370, 70), (60, 250), (380, 250), (220, 30)]
        svg = ("".join(f'<path id="{p}-n{i}" d="M{x} {y} L220 160" stroke="{LIGHT}" stroke-width="4" stroke-dasharray="1" pathLength="1" stroke-dashoffset="1"/>' for i, (x, y) in enumerate(nodes))
               + "".join(f'<circle id="{p}-o{i}" cx="{x}" cy="{y}" r="16" fill="{GOLD}"/>' for i, (x, y) in enumerate(nodes))
               + f'<g id="{p}-chip">' + "".join(f'<rect x="{168+i*28}" y="74" width="12" height="20" rx="3" fill="{PALE}"/><rect x="{168+i*28}" y="226" width="12" height="20" rx="3" fill="{PALE}"/>' for i in range(4))
               + f'<rect x="140" y="90" width="160" height="140" rx="22" fill="{BLUE}" stroke="#fff" stroke-width="5"/><text x="220" y="184" font-size="64" fill="#fff" text-anchor="middle" font-family="Poppins">AI</text></g>')
        js += [pop(f"#{p}-chip", t)] + [drawp(f"#{p}-n{i}", t + 0.3 + i * 0.1, 0.3) for i in range(5)] + [pop(f"#{p}-o{i}", t + 0.45 + i * 0.1, 0.3, 0) for i in range(5)] + \
              [f'tl.fromTo("#{p}-chip", {{ scale: 1 }}, {{ scale: 1.06, transformOrigin: "50% 50%", duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {t+0.6:.2f});']
    elif key == "techva":
        cols = [GOLD, LIGHT, GREEN, PALE, LIGHT]
        svg = (f'<rect x="70" y="30" width="300" height="196" rx="16" fill="{NAVY}" stroke="{PALE}" stroke-width="6"/><path d="M30 250 L410 250 L380 226 L60 226 Z" fill="{PALE}"/>'
               + "".join(f'<rect id="{p}-c{i}" x="{100 + (i % 3) * 24}" y="{60+i*30}" width="{[150,190,120,170,90][i]}" height="14" rx="7" fill="{cols[i]}"/>' for i in range(5))
               + f'<g id="{p}-tg"><rect x="250" y="262" width="150" height="46" rx="23" fill="{GOLD}"/><text x="325" y="293" font-size="24" fill="{NAVY}" text-anchor="middle" font-family="Poppins">&lt;/&gt;</text></g>')
        js += [grow(f"#{p}-c{i}", t + 0.1 + i * 0.16, 0.3, f"{100 + (i % 3) * 24} {67+i*30}") for i in range(5)] + [pop(f"#{p}-tg", t + 0.9)]
    elif key == "gears":
        svg = (f'<g id="{p}-g1"><path d="{gear_path(170, 180, 78, 10)}" fill="{LIGHT}"/><circle cx="170" cy="180" r="28" fill="{NAVY}"/></g>'
               f'<g id="{p}-g2"><path d="{gear_path(300, 100, 50, 8)}" fill="{GOLD}"/><circle cx="300" cy="100" r="18" fill="{NAVY}"/></g>'
               f'<g id="{p}-g3"><path d="{gear_path(318, 240, 40, 7)}" fill="{PALE}"/><circle cx="318" cy="240" r="14" fill="{NAVY}"/></g>')
        js += [pop(f"#{p}-g{i}", t + i * 0.12) for i in (1, 2, 3)]
        js += [f'tl.fromTo("#{p}-g1", {{ rotation: 0, svgOrigin: "170 180" }}, {{ rotation: 180, svgOrigin: "170 180", duration: 3, ease: "none", immediateRender: false }}, {t:.2f});',
               f'tl.fromTo("#{p}-g2", {{ rotation: 0, svgOrigin: "300 100" }}, {{ rotation: -280, svgOrigin: "300 100", duration: 3, ease: "none", immediateRender: false }}, {t:.2f});',
               f'tl.fromTo("#{p}-g3", {{ rotation: 0, svgOrigin: "318 240" }}, {{ rotation: -340, svgOrigin: "318 240", duration: 3, ease: "none", immediateRender: false }}, {t:.2f});']
    elif key == "hlplat":
        svg = (f'<circle id="{p}-ring" cx="220" cy="160" r="150" fill="none" stroke="{LIGHT}" stroke-width="4" stroke-dasharray="1" pathLength="1" stroke-dashoffset="1"/>'
               f'<image id="{p}-lg" href="assets/refs/highlevel-logo.png" x="40" y="120" width="360" height="81"/>')
        js += [drawp(f"#{p}-ring", t, 0.7), pop(f"#{p}-lg", t + 0.1, 0.5, 0.5)]
    # ---------- path-scene art ----------
    elif key == "onboard":
        svg = (f'<rect x="30" y="20" width="380" height="290" rx="22" fill="#fff"/><text x="60" y="66" font-size="24" fill="{NAVY}" font-family="Poppins">New account setup</text>'
               f'<rect x="60" y="86" width="320" height="24" rx="12" fill="{PALE}"/><rect id="{p}-pb" x="60" y="86" width="320" height="24" rx="12" fill="{GREEN}"/>'
               + "".join(f'<g id="{p}-k{i}"><circle cx="78" cy="{150+i*44}" r="14" fill="{GREEN}"/><path d="M71 {150+i*44} L76 {155+i*44} L86 {144+i*44}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
                         f'<rect x="104" y="{143+i*44}" width="{[170,130,150,110][i]}" height="14" rx="7" fill="#94A3B8"/></g>' for i in range(4))
               + f'<g id="{p}-rk"><path d="M340 290 C 340 240, 360 210, 370 196 C 380 210, 400 240, 400 290 Z" fill="{BLUE}" stroke="{NAVY}" stroke-width="4"/><circle cx="370" cy="240" r="10" fill="{PALE}"/>'
               f'<path d="M352 292 L362 316 L370 296 L378 316 L388 292 Z" fill="{GOLD}"/></g>')
        js += [grow(f"#{p}-pb", t + 0.3, 2.2, "60 98")] + [pop(f"#{p}-k{i}", t + 0.6 + i * 0.45) for i in range(4)] + \
              [f'tl.fromTo("#{p}-rk", {{ y: 0 }}, {{ y: -360, duration: 0.9, ease: "power2.in", immediateRender: false }}, {t+3.0:.2f});']
        sfx += [(t + 0.6 + i * 0.45, "49-click-tiny", 0.22) for i in range(4)] + [(t + 3.0, "whoosh-4", 0.24)]
    elif key == "socialphone":
        posts = "".join(f'<rect x="146" y="{40+i*96}" width="148" height="84" rx="12" fill="{[LIGHT, GOLD, PALE, LIGHT][i]}"/>' for i in range(4))
        hearts = "".join(f'<path id="{p}-h{i}" transform="translate({330+i*14} {250-i*6}) scale(0.9)" d="M20 8 C 20 -6, 0 -8, 0 6 C 0 -8, -20 -6, -20 8 C -20 22, 0 30, 0 36 C 0 30, 20 22, 20 8 Z" fill="{RED}"/>' for i in range(4))
        svg = (f'<defs><clipPath id="{p}-cp"><rect x="136" y="30" width="168" height="270" rx="16"/></clipPath></defs>'
               f'<rect x="124" y="10" width="192" height="304" rx="32" fill="{NAVY}" stroke="{PALE}" stroke-width="6"/>'
               f'<g clip-path="url(#{p}-cp)"><g id="{p}-fd">{posts}</g></g>{hearts}')
        js += [f'tl.fromTo("#{p}-fd", {{ y: 0 }}, {{ y: -110, duration: 3, ease: "sine.inOut" }}, {t:.2f});'] + \
              [f'tl.fromTo("#{p}-h{i}", {{ y: 0, opacity: 0 }}, {{ keyframes: [{{ opacity: 1, duration: 0.15 }}, {{ y: -170, opacity: 0, duration: 1.2, ease: "power1.out" }}] }}, {t+0.4+i*0.45:.2f});' for i in range(4)]
        sfx += [(t + 0.4 + i * 0.45, "30-blip-pop", 0.18) for i in range(0, 4, 2)]
    elif key == "workflow":
        nodes = [(70, 80, "FORM"), (180, 230, "SMS"), (290, 80, "TAG"), (390, 230, "EMAIL")]
        path = "M70 80 L180 230 L290 80 L390 230"
        svg = (f'<path id="{p}-wp" d="{path}" fill="none" stroke="{LIGHT}" stroke-width="6" stroke-dasharray="1" pathLength="1" stroke-dashoffset="1"/>'
               + "".join(f'<g id="{p}-n{i}"><circle cx="{x}" cy="{y}" r="40" fill="{NAVY}" stroke="{PALE}" stroke-width="5"/><circle id="{p}-on{i}" cx="{x}" cy="{y}" r="40" fill="{BLUE}" opacity="0"/>'
                         f'<text x="{x}" y="{y+7}" font-size="17" fill="#fff" text-anchor="middle" font-family="Poppins">{l}</text></g>' for i, (x, y, l) in enumerate(nodes))
               + f'<circle id="{p}-dot" cx="70" cy="80" r="11" fill="{GOLD}"/>')
        js += [pop(f"#{p}-n{i}", t + i * 0.12) for i in range(4)] + [drawp(f"#{p}-wp", t + 0.4, 1.2)]
        js += [f'tl.fromTo("#{p}-dot", {{ x: 0, y: 0, opacity: 0 }}, {{ keyframes: [{{ opacity: 1, duration: 0.05 }}, {{ x: 110, y: 150, duration: 0.6, ease: "none" }}, {{ x: 220, y: 0, duration: 0.6, ease: "none" }}, {{ x: 320, y: 150, duration: 0.6, ease: "none" }}] }}, {t+1.6:.2f});']
        js += [f'tl.fromTo("#{p}-on{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, {t+1.6+i*0.6:.2f});' for i in range(4)]
        sfx += [(t + 1.6 + i * 0.6, "49-click-tiny", 0.24) for i in range(4)]
    elif key == "clients":
        rows = ""
        for i in range(3):
            y = 30 + i * 92
            rows += (f'<g id="{p}-r{i}"><rect x="40" y="{y}" width="360" height="76" rx="16" fill="#fff"/><circle cx="84" cy="{y+38}" r="22" fill="{[LIGHT, GOLD, BLUE][i]}"/>'
                     f'<rect x="120" y="{y+22}" width="150" height="14" rx="7" fill="{NAVY}"/><rect x="120" y="{y+44}" width="100" height="10" rx="5" fill="#94A3B8"/>'
                     f'<circle cx="360" cy="{y+38}" r="16" fill="{RED}"/><circle id="{p}-g{i}" cx="360" cy="{y+38}" r="16" fill="{GREEN}" opacity="0"/></g>')
        svg = rows + f'<g id="{p}-tg"><rect x="110" y="300" width="220" height="16" rx="8" fill="none"/></g>'
        js += [slide(f"#{p}-r{i}", t + i * 0.15, x=60) for i in range(3)] + \
              [f'tl.fromTo("#{p}-g{i}", {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }}, {t+1.4+i*0.5:.2f});' for i in range(3)]
        sfx += [(t + 1.4 + i * 0.5, "24-ding-ring", 0.16) for i in range(3)]
    elif key == "coins":
        coins = "".join(f'<g id="{p}-c{i}"><ellipse cx="300" cy="{280-i*18}" rx="58" ry="16" fill="{GOLD}" stroke="#E0A400" stroke-width="4"/></g>' for i in range(7))
        svg = (f'<g id="{p}-lk"><rect x="40" y="110" width="110" height="60" rx="30" fill="none" stroke="{PALE}" stroke-width="14" transform="rotate(-35 95 140)"/>'
               f'<rect x="100" y="150" width="110" height="60" rx="30" fill="none" stroke="{LIGHT}" stroke-width="14" transform="rotate(-35 155 180)"/></g>'
               f'{coins}<text id="{p}-pc" x="300" y="100" font-size="72" fill="{GOLD}" text-anchor="middle" font-family="Poppins">40%</text>')
        js += [pop(f"#{p}-lk", t)] + [f'tl.fromTo("#{p}-c{i}", {{ y: -320, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "bounce.out" }}, {t+0.4+i*0.28:.2f});' for i in range(7)] + [pop(f"#{p}-pc", t + 0.3, 0.5, 2)]
        sfx += [(t + 0.4 + i * 0.28 + 0.3, "49-click-tiny", 0.22) for i in range(0, 7, 2)]
    elif key == "saas":
        users = "".join(f'<circle cx="{220 + math.cos(a) * 200:.0f}" cy="{170 + math.sin(a) * 140:.0f}" r="14" fill="{PALE}"/>' for a in [i * math.tau / 6 for i in range(6)])
        svg = (f'<g id="{p}-us">{users}</g>'
               f'<g id="{p}-bt"><rect x="70" y="190" width="300" height="96" rx="18" fill="#1e3a8a" stroke="{LIGHT}" stroke-width="4"/><image href="assets/refs/highlevel-logo.png" x="110" y="215" width="220" height="50"/></g>'
               f'<g id="{p}-tp"><rect x="70" y="70" width="300" height="104" rx="18" fill="{GOLD}"/><text x="220" y="134" font-size="36" fill="{NAVY}" text-anchor="middle" font-family="Poppins">YOUR BRAND</text></g>')
        js += [pop(f"#{p}-bt", t), f'tl.fromTo("#{p}-tp", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, ease: "back.out(1.6)" }}, {t+1.0:.2f});',
               f'tl.fromTo("#{p}-us", {{ rotation: 0, opacity: 0, svgOrigin: "220 170" }}, {{ rotation: 60, opacity: 1, svgOrigin: "220 170", duration: 4, ease: "none" }}, {t+0.4:.2f});']
        sfx += [(t + 1.0, "whoosh-1", 0.22)]
    else:
        raise KeyError(key)
    return svg, js, sfx


# --------------------------------------------------------------------------- CSS
CSS = """
.stage .stg { position: absolute; right: 56px; top: 150px; width: 500px; height: 490px; background: rgba(11, 32, 88, 0.95); border-radius: 26px; box-shadow: 0 24px 60px rgba(11, 32, 88, 0.35); overflow: hidden; }
.stage .stg .bar { position: absolute; left: 0; top: 0; bottom: 0; width: 10px; background: linear-gradient(180deg, var(--light), var(--blue)); }
.stage .stg .label { position: absolute; left: 40px; top: 26px; }
.stage .sc { position: absolute; left: 30px; top: 70px; width: 440px; }
.stage .sc svg { display: block; overflow: visible; }
.stage .cap2 { display: block; margin-top: 18px; text-align: center; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.1; color: #fff; white-space: nowrap; }
.stage .stampin { position: absolute; left: 50%; bottom: 34px; margin: 0; transform: translateX(-50%); }
.stage .chips { position: absolute; left: 40px; right: 30px; bottom: 26px; justify-content: center; }
.pscene .pwrap { position: absolute; inset: 0; overflow: hidden; }
.pscene .bg { position: absolute; inset: 0; background: radial-gradient(circle at 70% 45%, #1e40af 0%, #0b2058 55%, #071640 100%); }
.pscene .grid { position: absolute; inset: -80px; background-image: radial-gradient(rgba(234, 243, 255, 0.13) 2px, transparent 2.5px); background-size: 44px 44px; }
.pscene .ghost { position: absolute; right: -40px; bottom: -150px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 720px; line-height: 1; color: rgba(234, 243, 255, 0.05); }
.pscene .tblock { position: absolute; left: 140px; top: 210px; width: 820px; }
.pscene .tblock .label { font-size: 24px; }
.pscene .pnum { display: flex; align-items: baseline; gap: 16px; }
.pscene .pnum b { font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 230px; line-height: 0.95; color: #fff; }
.pscene .pnum span { font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 64px; color: var(--light); }
.pscene .ptitle { display: block; margin-top: 10px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 82px; line-height: 1.04; color: #fff; }
.pscene .ptitle em { font-style: normal; color: var(--gold); }
.pscene .psub2 { display: block; margin-top: 18px; font-weight: 700; font-size: 30px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--pale); }
.pscene .mrow2 { display: flex; align-items: flex-end; gap: 22px; margin-top: 34px; }
.pscene .mrow2 .mlab { font-weight: 700; font-size: 20px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--pale); }
.pscene .meter.big { gap: 9px; }
.pscene .meter.big i { width: 30px; }
.pscene .gart { position: absolute; right: 90px; top: 210px; width: 800px; height: 582px; }
.pscene .gart svg { overflow: visible; }
.pscene .hire { position: absolute; right: 120px; top: 170px; padding: 10px 26px; border: 8px solid var(--gold); border-radius: 18px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 64px; color: var(--gold); background: rgba(11, 32, 88, 0.9); }
.kin .kt { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.kin .k7 { display: block; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 300px; line-height: 0.9; color: var(--gold); }
.kin .klogo { display: block; width: 760px; margin-top: 14px; }
.kin .kw2 { display: block; margin-top: 18px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 120px; line-height: 1; color: #fff; letter-spacing: 0.02em; }
.kin .kw2 span { display: inline-block; }
.kin .kw3 { display: block; margin-top: 22px; font-weight: 700; font-size: 44px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--pale); }
.kin svg.streams { position: absolute; inset: 0; }
.hub2 .hbg { position: absolute; right: 0; top: 0; bottom: 0; width: 860px; background: linear-gradient(90deg, rgba(11, 32, 88, 0) 0%, rgba(11, 32, 88, 0.92) 14%, #0b2058 40%, #0e2a6e 100%); }
.hub2 .hwrap { position: absolute; right: 20px; top: 150px; width: 740px; height: 640px; }
.hub2 .hlab { position: absolute; left: 0; right: 0; top: 0; text-align: center; font-weight: 700; font-size: 24px; letter-spacing: 0.16em; text-transform: uppercase; color: #fff; text-shadow: 0 2px 10px rgba(11, 32, 88, 0.9); }
.hub2 .hways { position: absolute; left: 0; right: 0; bottom: -30px; text-align: center; }
.hub2 .hways span { display: inline-block; background: rgba(11, 32, 88, 0.94); border-radius: 999px; padding: 12px 30px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 34px; }
.hub2 .hways b { color: var(--gold); }
.conf .chip2 { position: absolute; right: 56px; top: 48px; background: var(--gold); color: var(--navy); border-radius: 16px; padding: 12px 28px; font-family: "Poppins", Arial, sans-serif; font-weight: 800; font-size: 46px; letter-spacing: 0.04em; }
.conf .q { position: absolute; font-family: "Poppins", Arial, sans-serif; font-weight: 800; color: #fff; text-shadow: 0 6px 20px rgba(11, 32, 88, 0.6); }
.wipe .wb { position: absolute; top: -200px; height: 1480px; width: 420px; }
"""


def meter_big(n):
    out = []
    for k in range(1, 8):
        h = 30 + k * 16
        c = "now" if k == n else ("on" if k < n else "")
        out.append(f'<i class="{c}" style="height:{h}px"></i>')
    return f'<div class="meter big">{"".join(out)}</div>'


def stage(H, J, SFX, sid, a, b, label, scenes, track=1, tail_html="", tail_js=()):
    """Right-side card whose illustration swaps with each spoken item. scenes: [(key, caption, t, extra)]"""
    inner, js, sfx = "", [], []
    for i, (key, cap, t, ex) in enumerate(scenes):
        p = f"{sid}{i}"
        svg, ijs, isfx = ill(key, p, t, ex)
        inner += f'<div class="sc" id="{p}"><svg viewBox="0 0 440 320" width="440" height="320">{svg}</svg><span class="cap2">{cap}</span></div>'
        js.append(f'tl.set("#{p}", {{ opacity: 0 }}, {a});')
        js.append(f'tl.fromTo("#{p}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "{E}", immediateRender: false }}, {t-0.1:.2f});')
        nxt = scenes[i + 1][2] if i + 1 < len(scenes) else None
        if nxt is not None:
            js.append(f'tl.to("#{p}", {{ opacity: 0, y: -24, duration: 0.25, ease: "power2.in" }}, {nxt-0.32:.2f});')
        js += ijs
        sfx += [(round(t - 0.12, 2), "whoosh-1", 0.18, f"{sid} scene")] + [(round(x, 2), s, v, f"{sid} ill") for x, s, v in isfx]
    H.append(f'<div id="{sid}" class="clip stage" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="{track}"><div class="stg"{' style="height: 570px"' if tail_html else ''}><div class="bar"></div><span class="label">{label}</span>{inner}{tail_html}</div></div>')
    J.append(f'tl.fromTo("#{sid} .stg", {{ x: 120, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.55, ease: "{E}" }}, {a});')
    J.append(f'tl.to("#{sid} .stg", {{ x: 90, opacity: 0, duration: 0.4, ease: "power2.in" }}, {b-0.4:.2f});')
    J.extend(js)
    J.extend(tail_js)
    SFX.extend([(round(a - 0.05, 2), "whoosh-4", 0.28, f"{sid} in"), (round(b - 0.42, 2), "whoosh-2", 0.2, f"{sid} out")] + sfx)


def pscene(H, J, SFX, n, a, b, title, sub, key, stamp=None):
    p = f"ps{n}"
    svg, ijs, isfx = ill(key, f"{p}a", a + 0.7)
    stamp_html = f'<span class="hire" id="{p}-st">{stamp}</span>' if stamp else ""
    H.append(f'''<div id="{p}" class="clip pscene" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="11"><div class="pwrap" id="{p}-w">
<div class="bg" id="{p}-bg"></div><div class="grid" id="{p}-gr"></div><span class="ghost">0{n}</span>
<div class="tblock"><span class="label" id="{p}-lb">Path</span><div class="pnum" id="{p}-nm"><b>0{n}</b><span>/ 07</span></div>
<span class="ptitle" id="{p}-tt">{title}</span><span class="psub2" id="{p}-sb">{sub}</span>
<div class="mrow2" id="{p}-mr"><span class="mlab">Experience needed</span>{meter_big(n)}</div></div>
<div class="gart"><svg viewBox="0 0 440 320" width="800" height="582">{svg}</svg></div>{stamp_html}</div></div>''')
    J.extend([
        f'tl.fromTo("#{p}-bg", {{ clipPath: "circle(0% at 30% 45%)" }}, {{ clipPath: "circle(140% at 30% 45%)", duration: 0.55, ease: "power2.inOut" }}, {a});',
        f'tl.fromTo("#{p}-gr", {{ x: 0, y: 0 }}, {{ x: -44, y: -44, duration: {b-a:.2f}, ease: "none" }}, {a});',
        f'tl.fromTo("#{p}-lb", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "{E}" }}, {a+0.2:.2f});',
        f'tl.fromTo("#{p}-nm b", {{ scale: 2.4, opacity: 0, transformOrigin: "0% 80%" }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" }}, {a+0.2:.2f});',
        f'tl.fromTo("#{p}-nm span", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "{E}" }}, {a+0.45:.2f});',
        f'tl.fromTo("#{p}-tt", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "{E}" }}, {a+0.5:.2f});',
        f'tl.fromTo("#{p}-sb", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "{E}" }}, {a+0.8:.2f});',
        f'tl.fromTo("#{p}-mr", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a+1.0:.2f});',
        f'tl.fromTo("#{p}-mr .meter i", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.07 }}, {a+1.05:.2f});',
        f'tl.fromTo("#{p}-mr .meter i.now", {{ scaleX: 1 }}, {{ scaleX: 1.35, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {a+1.7:.2f});',
        f'tl.to("#{p}-w", {{ opacity: 0, duration: 0.35, ease: "power1.in" }}, {b-0.35:.2f});',
    ] + ijs)
    if stamp:
        J.append(f'tl.fromTo("#{p}-st", {{ scale: 2.4, opacity: 0, rotation: -18 }}, {{ scale: 1, opacity: 1, rotation: -6, duration: 0.4, ease: "back.out(2.2)" }}, {a+2.2:.2f});')
        SFX.append((round(a + 2.2, 2), "26-hit-short", 0.26, f"path {n} stamp"))
    SFX.extend([(round(a - 0.05, 2), "08-boom-swoosh", 0.3, f"path {n} in"), (round(a + 0.2, 2), "06-impact-punch", 0.3, f"path {n} number"),
                (round(b - 0.4, 2), "whoosh-2", 0.2, f"path {n} out")]
               + [(round(a + 1.05 + 0.07 * k, 2), "49-click-tiny", 0.16, "meter") for k in range(n)]
               + [(round(x, 2), s, v, f"path {n} art") for x, s, v in isfx])


def kinetic(H, J, SFX, a=11.3, b=16.0):
    streams = ""
    cols = ["#FFC531", "#3882F6", "#22C55E", "#EAF3FF", "#60A5FA", "#F59E0B", "#2563EB"]
    for i in range(7):
        y = 140 + i * 130
        streams += f'<path id="kst{i}" d="M-50 {y} C 400 {y-90}, 700 {y+90}, 1000 {y} S 1600 {y-90}, 1980 {y}" fill="none" stroke="{cols[i]}" stroke-width="6" stroke-linecap="round" opacity="0.35" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    H.append(f'''<div id="kin" class="clip pscene kin" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="11"><div class="pwrap" id="kin-w">
<div class="bg" id="kin-bg"></div><div class="grid" id="kin-gr"></div><svg class="streams" width="1920" height="1080" viewBox="0 0 1920 1080">{streams}</svg>
<div class="kt" id="kin-kt"><span class="k7" id="k7">7</span><img class="klogo" id="klogo" src="assets/refs/highlevel-logo.png" alt="HighLevel" />
<span class="kw2"><span id="kwa">INCOME</span> <span id="kwb">STREAMS</span></span><span class="kw3" id="kw3">for virtual assistants</span></div></div></div>''')
    J.extend([
        f'tl.fromTo("#kin-bg", {{ clipPath: "circle(0% at 50% 50%)" }}, {{ clipPath: "circle(150% at 50% 50%)", duration: 0.6, ease: "power2.inOut" }}, {a});',
        f'tl.fromTo("#kin-gr", {{ x: 0, y: 0 }}, {{ x: -44, y: 44, duration: {b-a:.2f}, ease: "none" }}, {a});',
        f'tl.fromTo("#kin-kt", {{ scale: 1 }}, {{ scale: 1.06, duration: {b-a:.2f}, ease: "none" }}, {a});',
        "for (let i = 0; i < 7; i++) " + f'tl.fromTo("#kst" + i, {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 1.6, ease: "power2.out" }}, {12.9:.2f} + i * 0.1);',
        f'tl.fromTo("#k7", {{ scale: 3.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, 12.15);',
        f'tl.fromTo("#klogo", {{ y: 50, opacity: 0, scale: 0.8 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, 12.35);',
        f'tl.fromTo("#kwa", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "{E}" }}, 12.95);',
        f'tl.fromTo("#kwb", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "{E}" }}, 13.35);',
        f'tl.fromTo("#kw3", {{ scaleX: 1.4, opacity: 0 }}, {{ scaleX: 1, opacity: 1, duration: 0.6, ease: "{E}" }}, 14.0);',
        f'tl.to("#kin-w", {{ opacity: 0, scale: 1.08, duration: 0.35, ease: "power1.in" }}, {b-0.35:.2f});',
    ])
    SFX.extend([(round(a - 0.05, 2), "whoosh-7", 0.38, "kinetic in"), (12.15, "06-impact-punch", 0.32, "7"), (12.35, "30-blip-pop", 0.3, "logo"),
                (12.95, "43-click-tonal", 0.28, "income"), (13.35, "60-blip-tonal", 0.28, "streams"), (14.0, "45-swish-short", 0.24, "for VAs"),
                (round(b - 0.4, 2), "whoosh-2", 0.22, "kinetic out")])


def hub(H, J, SFX, a=0.35, b=9.0):
    tiles = ["CRM", "EMAIL", "SMS", "CALENDAR", "FUNNELS", "SOCIAL"]
    cx, cy = 400, 330
    lines, tg, dots = "", "", ""
    for k, t in enumerate(tiles):
        ang = -math.pi / 2 + k * math.pi / 3
        x, y = cx + math.cos(ang) * 300, cy + math.sin(ang) * 220
        lines += f'<path id="hl{k}" d="M{x:.0f} {y:.0f} L{cx} {cy}" stroke="#3882F6" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
        dots += f'<circle id="hd{k}" cx="{x:.0f}" cy="{y:.0f}" r="8" fill="#FFC531" opacity="0"/>'
        tg += (f'<g id="ht{k}"><rect x="{x-82:.0f}" y="{y-30:.0f}" width="164" height="60" rx="16" fill="#EAF3FF" stroke="#2563EB" stroke-width="4"/>'
               f'<text x="{x:.0f}" y="{y+9:.0f}" font-size="24" fill="#0B2058" text-anchor="middle" font-family="Poppins">{t}</text></g>')
    H.append(f'''<div id="hub" class="clip hub2" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="1"><div class="hbg" id="hub-bg"></div><div class="hwrap" id="hub-w">
<svg width="740" height="610" viewBox="0 0 800 660" style="position:absolute;left:0;top:0;overflow:visible">{lines}{dots}
<g id="hcore"><circle cx="{cx}" cy="{cy}" r="150" fill="#0B2058" stroke="#3882F6" stroke-width="6"/><circle id="hpulse" cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#FFC531" stroke-width="5" opacity="0"/>
<image href="assets/refs/highlevel-logo.png" x="{cx-128}" y="{cy-29}" width="256" height="58"/></g>{tg}</svg>
<span class="hlab" id="hub-lab">All-in-one marketing platform</span><div class="hways" id="hub-ways"><span>So many ways to <b>earn</b></span></div></div></div>''')
    J.extend([
        f'tl.fromTo("#cam", {{ x: 0 }}, {{ x: -380, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {a});',
        f'tl.fromTo("#cam", {{ x: -380 }}, {{ x: 0, duration: 0.6, ease: "power3.inOut", immediateRender: false }}, {b-0.6:.2f});',
        f'tl.fromTo("#hub-bg", {{ x: 860 }}, {{ x: 0, duration: 0.7, ease: "power3.inOut" }}, {a});',
        f'tl.to("#hub-bg", {{ x: 860, duration: 0.6, ease: "power3.inOut" }}, {b-0.6:.2f});',
        f'tl.fromTo("#hcore", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.6, ease: "back.out(1.8)" }}, {a+0.4:.2f});',
        f'tl.fromTo("#hub-lab", {{ y: -20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "{E}" }}, {a+0.7:.2f});',
        "for (let k = 0; k < 6; k++) { "
        f'tl.fromTo("#hl" + k, {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, 1.3 + k * 0.2); '
        f'tl.fromTo("#ht" + k, {{ scale: 0.3, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, 1.45 + k * 0.2); '
        f'tl.fromTo("#hd" + k, {{ x: 0, y: 0, opacity: 0 }}, {{ keyframes: [{{ opacity: 1, duration: 0.05 }}, {{ x: {cx} - Number(document.getElementById("hd" + k).getAttribute("cx")), y: {cy} - Number(document.getElementById("hd" + k).getAttribute("cy")), duration: 0.7, ease: "power1.in" }}, {{ opacity: 0, duration: 0.05 }}] }}, 3.4 + k * 0.12); }}',
        f'tl.fromTo("#hpulse", {{ opacity: 0.9, scale: 1, transformOrigin: "50% 50%" }}, {{ opacity: 0, scale: 1.35, duration: 0.8, ease: "power2.out", immediateRender: false }}, 4.5);',
        f'tl.fromTo("#hub-ways", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "{E}" }}, 6.8);',
        f'tl.to("#hub-w", {{ opacity: 0, x: 80, duration: 0.45, ease: "power2.in" }}, {b-0.45:.2f});',
    ])
    SFX.extend([(0.0, "08-boom-swoosh", 0.4, "intro swipe"), (a + 0.4, "30-blip-pop", 0.3, "hub core")]
               + [(round(1.45 + k * 0.2, 2), "49-click-tiny", 0.22, "tile") for k in range(6)]
               + [(4.5, "24-ding-ring", 0.2, "all in one"), (6.8, "43-click-tonal", 0.28, "ways to earn"), (round(b - 0.45, 2), "whoosh-2", 0.2, "hub out")])


def confused(H, J, SFX, a=54.35, dur=6.87):
    b = round(a + dur, 2)
    H.append(f'<video id="conf-v" class="clip" src="assets/broll/confused.mp4" muted playsinline data-start="{a}" data-duration="{dur}" data-track-index="13" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover"></video>')
    qs = "".join(f'<span class="q" id="cq{i}" style="left:{x}px; top:{y}px; font-size:{s}px">?</span>' for i, (x, y, s) in enumerate([(380, 140, 140), (1500, 260, 110), (260, 520, 90)]))
    H.append(f'<div id="conf" class="clip conf" data-start="{a}" data-duration="{dur}" data-track-index="14"><span class="chip2" id="conf-chip">Confused</span>{qs}</div>')
    for wid, t0 in (("cw1", a - 0.3), ("cw2", b - 0.3)):
        H.append(f'<div id="{wid}" class="clip wipe" data-start="{t0:.2f}" data-duration="0.65" data-track-index="5"><div class="wb" id="{wid}a" style="left:-1000px;background:#2563EB"></div><div class="wb" id="{wid}b" style="left:-1450px;background:#0B2058"></div></div>')
        J.append(f'tl.fromTo(["#{wid}a", "#{wid}b"], {{ x: 0, skewX: -16 }}, {{ x: 3600, skewX: -16, duration: 0.6, ease: "power2.inOut", stagger: 0.05 }}, {t0:.2f});')
        SFX.append((round(t0, 2), "whoosh-3", 0.28, "confused wipe"))
    J.extend([f'tl.fromTo("#conf-chip", {{ scale: 2, opacity: 0, rotation: -12 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: 0.4, ease: "back.out(2.2)" }}, {a+0.35:.2f});',
              f'tl.to("#conf-chip", {{ opacity: 0, duration: 0.3 }}, {b-0.35:.2f});']
             + [f'tl.fromTo("#cq{i}", {{ scale: 0, opacity: 0, rotation: -30 }}, {{ scale: 1, opacity: 1, rotation: {[-12, 14, -6][i]}, duration: 0.45, ease: "back.out(2.5)" }}, {a+1.0+i*0.7:.2f});' for i in range(3)]
             + [f'tl.fromTo("#cq{i}", {{ y: 0 }}, {{ y: -14, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {a+1.5+i*0.7:.2f});' for i in range(3)]
             + [f'tl.to("#cq{i}", {{ opacity: 0, duration: 0.3 }}, {b-0.35:.2f});' for i in range(3)])
    SFX.extend([(round(a + 0.35, 2), "26-hit-short", 0.26, "confused chip")] + [(round(a + 1.0 + i * 0.7, 2), "40-boing-down", 0.18, "?") for i in range(3)])
