"""Animated header banner: HS monogram in a hexagon, name, and roles typed in a loop."""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from textpath import mono_advance, text_path, text_width  # noqa: E402

W, H = 1000, 260
CYAN, GOLD, INK = "#22D3EE", "#F5B83D", "#E6EDF3"

PHRASES = [
    "IT Risk & Governance Analyst @ Bradesco",
    "Security engineering: PKI · mTLS · SIEM",
    "Computer Engineering student @ FIAP",
    "Building secure tech, from São Paulo to Luanda",
]

# ---------------------------------------------------------------- typing timeline
TYPE, HOLD, DEL, GAP = 0.055, 2.3, 0.022, 0.35
SIZE = 21
CW = mono_advance(SIZE)
PX = 240 + round(mono_advance(21, "mono-b") * 3)  # typed text starts after "~$ "
BASE_Y = 172


def timeline():
    slots, t = [], 0.4
    for p in PHRASES:
        n = len(p)
        start = t
        t += n * TYPE + HOLD + n * DEL + GAP
        slots.append((start, n))
    return slots, t


SLOTS, T = timeline()


def frames_for(i):
    """(time, visible_chars) for phrase i over the whole cycle."""
    start, n = SLOTS[i]
    fr = [(0.0, 0)]
    for k in range(1, n + 1):
        fr.append((start + k * TYPE, k))
    end_type = start + n * TYPE
    for k in range(1, n + 1):
        fr.append((end_type + HOLD + k * DEL, n - k))
    return fr


def smil(fr, fmt):
    kt = ";".join(f"{t / T:.5f}" for t, _ in fr)
    vals = ";".join(fmt(v) for _, v in fr)
    return f'values="{vals}" keyTimes="{kt}"'


def cursor_frames():
    """Cursor x follows whichever phrase is active."""
    fr = [(0.0, 0)]
    for i in range(len(PHRASES)):
        fr += [f for f in frames_for(i)[1:]]
    fr.sort()
    return fr


# ---------------------------------------------------------------- hexagon logo
CX, CY, R = 128, 130, 78


def hex_points(r, cx=CX, cy=CY):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in range(-90, 270, 60)]


def hex_path(r):
    pts = hex_points(r)
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


PERIM = 6 * R


def build():
    hs = text_path("HS", "display-xb", 58, CX, CY + 21, spacing=-1, anchor="middle")
    name = text_path("Henriques Soares", "display-xb", 56, 240, 112, spacing=-0.6)
    prompt = text_path("~$", "mono-b", SIZE, 240, BASE_Y)
    meta_text = "SÃO PAULO, BRAZIL   ·   ANGOLAN ROOTS   ·   SECURITY · GRC · CLOUD"
    meta = text_path(meta_text, "inter-sb", 11.5, 241, 216, spacing=1.6)
    pill = text_path("SECURE BY DESIGN", "inter-sb", 10.5, 32, 18, spacing=1.7)

    typed = []
    for i, p in enumerate(PHRASES):
        d = text_path(p, "mono", SIZE, PX, BASE_Y)
        typed.append(f'''
    <clipPath id="clip{i}"><rect x="{PX - 1}" y="{BASE_Y - 22}" height="30" width="0">
      <animate attributeName="width" dur="{T:.3f}s" repeatCount="indefinite" calcMode="discrete" {smil(frames_for(i), lambda v: f"{v * CW + (1 if v else 0):.2f}")}/>
    </rect></clipPath>''')
    typed_defs = "".join(typed)
    typed_paths = "".join(
        f'<path clip-path="url(#clip{i})" d="{text_path(p, "mono", SIZE, PX, BASE_Y)}" fill="url(#typeGrad)"/>'
        for i, p in enumerate(PHRASES))

    cur = smil(cursor_frames(), lambda v: f"{PX + v * CW + 2:.2f}")

    # circuit traces leaving the logo, with packets running on them
    traces = [
        ("M210,62 H860 L900,34 H980", 7.5, CYAN, 0.0),
        ("M214,200 H560 L590,228 H980", 9.0, GOLD, 1.2),
        ("M40,236 H120 L150,206", 5.0, CYAN, 2.4),
        ("M700,236 H980", 6.0, CYAN, 3.1),
    ]
    trace_svg = []
    for k, (d, dur, col, begin) in enumerate(traces):
        trace_svg.append(f'<path id="tr{k}" d="{d}" fill="none" stroke="#17324A" stroke-width="1.2"/>')
        trace_svg.append(
            f'<circle r="2.6" fill="{col}" filter="url(#glow)" opacity="0.9">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath href="#tr{k}"/></animateMotion></circle>')

    hex_outer = hex_path(R)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Henriques Soares — IT Risk &amp; Governance, Security Engineering">
  <title>Henriques Soares — IT Risk &amp; Governance · Security Engineering</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#060A12"/><stop offset="1" stop-color="#0C1828"/>
    </linearGradient>
    <radialGradient id="glowC" cx="0.12" cy="0.2" r="0.55"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowG" cx="0.92" cy="1" r="0.6"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.16"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
    <linearGradient id="hexGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{GOLD}"/>
    </linearGradient>
    <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#FFFFFF"/>
      <stop offset="0.5" stop-color="#BDF4FF"/><stop offset="0.55" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D7E3EF"/>
      <animate attributeName="x1" values="-1;1.4" dur="6s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="0;2.4" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="typeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#A5F3FC"/><stop offset="1" stop-color="#67E8F9"/>
    </linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.1" fill="#1B2638"/>
    </pattern>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>{typed_defs}
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.8"/>
    <rect width="{W}" height="{H}" fill="url(#glowC)"/>
    <rect width="{W}" height="{H}" fill="url(#glowG)"/>
    {"".join(trace_svg)}

    <!-- monogram -->
    <path d="{hex_path(R + 10)}" fill="none" stroke="url(#hexGrad)" stroke-width="10" opacity="0.18" filter="url(#soft)">
      <animate attributeName="opacity" values="0.10;0.28;0.10" dur="4s" repeatCount="indefinite"/>
    </path>
    <path d="{hex_path(R - 2)}" fill="#0A1524" opacity="0.92"/>
    <path id="hexRing" d="{hex_outer}" fill="none" stroke="url(#hexGrad)" stroke-width="3" stroke-linejoin="round"
          stroke-dasharray="{PERIM}" stroke-dashoffset="{PERIM}">
      <animate attributeName="stroke-dashoffset" from="{PERIM}" to="0" dur="1.6s" begin="0.1s" fill="freeze"/>
    </path>
    <path d="{hex_path(R - 12)}" fill="none" stroke="#1E3A52" stroke-width="1" stroke-dasharray="3 5"/>
    <path d="{hs}" fill="url(#hexGrad)" opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="0.9s" fill="freeze"/>
    </path>
    <circle r="4" fill="{GOLD}" filter="url(#glow)">
      <animateMotion dur="6s" begin="1.7s" repeatCount="indefinite" rotate="auto"><mpath href="#hexRing"/></animateMotion>
    </circle>

    <!-- name -->
    <path d="{name}" fill="url(#nameGrad)" opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="0.4s" fill="freeze"/>
    </path>

    <!-- typed roles -->
    <path d="{prompt}" fill="{GOLD}"/>
    {typed_paths}
    <rect y="{BASE_Y - 18}" width="{CW * 0.62:.2f}" height="22" rx="1.5" fill="{CYAN}">
      <animate attributeName="x" dur="{T:.3f}s" repeatCount="indefinite" calcMode="discrete" {cur}/>
      <animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
    </rect>

    <!-- meta line -->
    <path d="M241,196 H{241 + 60}" stroke="url(#hexGrad)" stroke-width="2" stroke-linecap="round"/>
    <path d="{meta}" fill="#7D8EA3"/>

    <!-- status pill -->
    <g transform="translate({W - 214},22)">
      <rect width="190" height="28" rx="14" fill="#0A1524" stroke="#1E3A52"/>
      <circle cx="17" cy="14" r="4" fill="#3FB950"><animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <circle cx="17" cy="14" r="4" fill="none" stroke="#3FB950"><animate attributeName="r" values="4;10" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>
      <path d="{pill}" fill="#9FB3C8"/>
    </g>
    <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#1B2A3D"/>
  </g>
</svg>
'''
    return svg


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "assets" / "header.svg")
    s = build()
    open(out, "w").write(s)
    print(out, len(s), "bytes; cycle", round(T, 2), "s; widest phrase px",
          round(max(len(p) for p in PHRASES) * CW), "name px", round(text_width("Henriques Soares", "display-xb", 56, -0.6)))
