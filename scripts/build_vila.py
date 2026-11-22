"""Animated architecture diagram for the Vila Aurora project."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from textpath import text_path  # noqa: E402

W, H = 1000, 424
CYAN, GOLD, GREEN, RED = "#22D3EE", "#F5B83D", "#3FB950", "#F85149"
BOX, STROKE, SUB, INK = "#0F1B2D", "#1E3A52", "#8FA3B8", "#E6EDF3"
CYCLE = 9.0


def t(text, font, size, x, y, fill, spacing=0.0, anchor="start", extra=""):
    return f'<path d="{text_path(text, font, size, x, y, spacing, anchor)}" fill="{fill}" {extra}/>'


def box(x, y, w, h, stroke=STROKE, fill=BOX, rx=12, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'


def window(start, end, fade=0.08):
    """opacity keyframes visible between start and end seconds of the cycle."""
    a, b = start / CYCLE, end / CYCLE
    f = fade / CYCLE
    return (f'values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a + f:.4f};{b - f:.4f};{b:.4f};1" '
            f'dur="{CYCLE}s" repeatCount="indefinite"')


def one_shot_motion(path_id, start, end, color, r=4.5):
    a, b = start / CYCLE, end / CYCLE
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)" opacity="0">'
            f'<animate attributeName="opacity" {window(start, end, 0.05)}/>'
            f'<animateMotion dur="{CYCLE}s" repeatCount="indefinite" calcMode="linear" '
            f'keyPoints="0;0;1;1" keyTimes="0;{a:.4f};{b:.4f};1"><mpath href="#{path_id}"/></animateMotion></circle>')


def loop_packet(path_id, dur, begin, color=GREEN, r=3.6):
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath href="#{path_id}"/></animateMotion></circle>')


def build():
    out = []
    # ---------------------------------------------------------------- header
    out.append(t("VILA AURORA", "display-b", 17, 28, 40, INK, spacing=2.2))
    out.append(t("Secure, resilient infrastructure for a community network  ·  FIAP Global Solution 2026",
                 "inter-m", 12, 28, 62, SUB))
    lx = 686
    for i, (label, col) in enumerate((("telemetry", GREEN), ("blocked attack", RED), ("SIEM alert", GOLD))):
        x = lx + [0, 96, 216][i]
        out.append(f'<circle cx="{x}" cy="36" r="4.5" fill="{col}"/>')
        out.append(t(label, "inter-m", 11.5, x + 10, 40, SUB))

    # ---------------------------------------------------------------- field devices
    spaces = ["School", "Health unit (UBS)", "Shelter", "Garden & kitchen", "Community center"]
    fy = [96, 134, 172, 210, 248]
    for i, (name, y) in enumerate(zip(spaces, fy)):
        out.append(box(28, y, 172, 30, rx=9))
        out.append(f'<circle cx="44" cy="{y + 15}" r="4" fill="{GREEN}"><animate attributeName="opacity" '
                   f'values="1;0.35;1" dur="2s" begin="{i * 0.4}s" repeatCount="indefinite"/></circle>')
        out.append(t(name, "inter-sb", 11.5, 56, y + 19.5, INK))
        out.append(t("x509", "mono", 9, 192, y + 18.5, CYAN, anchor="end", extra='opacity="0.8"'))
        pid = f"f{i}"
        out.append(f'<path id="{pid}" d="M200,{y + 15} C232,{y + 15} 232,193 262,193" fill="none" '
                   f'stroke="#1E3A52" stroke-width="1.3"/>')
    out.append(t("FIELD · 1 certificate per device", "inter-sb", 10, 28, 296, SUB, spacing=0.8))

    # ---------------------------------------------------------------- edge node
    out.append(box(262, 100, 200, 186, stroke="#235070"))
    out.append(t("EDGE NODE", "display-b", 12.5, 280, 126, CYAN, spacing=1.6))
    rows = [("MQTT broker", "mTLS + per-device ACL"), ("Local rules", "keeps working offline"),
            ("Store & forward", "no data lost on link drop")]
    for i, (a, b) in enumerate(rows):
        y = 152 + i * 42
        out.append(f'<rect x="280" y="{y - 13}" width="3" height="30" rx="1.5" fill="{CYAN}" opacity="0.6"/>')
        out.append(t(a, "inter-sb", 12, 292, y, INK))
        out.append(t(b, "inter-m", 10.5, 292, y + 15, SUB))

    # ---------------------------------------------------------------- tunnel
    out.append('<path id="tun" d="M462,170 H656" fill="none"/>')
    out.append(f'<rect x="474" y="152" width="154" height="36" rx="18" fill="#0A1524" stroke="{CYAN}" stroke-opacity="0.55"/>')
    out.append(f'<path d="M492,170 H612" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="6 7">'
               f'<animate attributeName="stroke-dashoffset" from="26" to="0" dur="0.8s" repeatCount="indefinite"/></path>')
    # lock icon
    out.append('<g transform="translate(543,122)" fill="none" stroke="#F5B83D" stroke-width="2">'
               '<path d="M3,9 V6 a5,5 0 0 1 10,0 V9"/><rect x="0" y="9" width="16" height="12" rx="3" fill="#F5B83D" stroke="none"/></g>')
    out.append(t("WireGuard tunnel", "inter-sb", 11.5, 551, 117, INK, anchor="middle"))
    out.append(t("ChaCha20-Poly1305", "mono", 9.5, 551, 206, SUB, anchor="middle"))

    # ---------------------------------------------------------------- cloud
    out.append(box(640, 100, 332, 186, stroke="#235070"))
    out.append(t("CLOUD", "display-b", 12.5, 658, 126, CYAN, spacing=1.6))
    out.append(box(656, 142, 300, 56, fill="#0B1626", rx=9))
    out.append(t("Ingest API", "inter-sb", 12, 672, 166, INK))
    out.append(t("mTLS + CRL · listens only inside the tunnel", "inter-m", 10.5, 672, 183, SUB))
    out.append(box(656, 214, 300, 56, fill="#0B1626", rx=9))
    out.append(t("PostgreSQL", "inter-sb", 12, 672, 238, INK))
    out.append(t("least-privilege roles · append-only audit", "inter-m", 10.5, 672, 255, SUB))
    out.append('<path id="db" d="M806,198 V214" fill="none"/>')

    # ---------------------------------------------------------------- SIEM + panel
    out.append('<path id="logs" d="M690,286 V316" fill="none" stroke="#1E3A52" stroke-dasharray="3 4"/>')
    out.append('<path d="M870,286 V316" fill="none" stroke="#1E3A52" stroke-dasharray="3 4"/>')
    out.append(box(470, 316, 240, 84, stroke=STROKE, extra='id="siemBox"'))
    out.append(f'<rect x="470" y="316" width="240" height="84" rx="12" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">'
               f'<animate attributeName="opacity" {window(4.0, 7.2)}/></rect>')
    out.append(t("SIEM", "display-b", 12.5, 488, 342, CYAN, spacing=1.6))
    out.append(t("4 detection rules · MITRE ATT&CK", "inter-m", 10.5, 488, 360, SUB))
    out.append(t("auto-contains low risk · human approval for high impact", "inter-m", 9, 488, 378, SUB,
                 extra='opacity="0.85"'))
    # alert pill
    out.append(f'<g opacity="0"><animate attributeName="opacity" {window(4.0, 7.2)}/>'
               f'<rect x="566" y="329" width="132" height="20" rx="10" fill="{GOLD}" fill-opacity="0.15" stroke="{GOLD}"/>'
               + t("ALERT · Rule C · T1190", "mono-b", 9.5, 632, 343, GOLD, anchor="middle") + "</g>")

    out.append(box(732, 316, 240, 84))
    out.append(t("SUPERVISION PANEL", "display-b", 12.5, 750, 342, CYAN, spacing=1.6))
    out.append(t("password + TOTP MFA · RBAC", "inter-m", 10.5, 750, 360, SUB))
    out.append(t("CSRF protection · full audit trail", "inter-m", 9.5, 750, 378, SUB, extra='opacity="0.85"'))

    # ---------------------------------------------------------------- attacker
    out.append(box(28, 340, 172, 56, stroke=RED, fill="#1A0F14", extra='stroke-dasharray="5 4" stroke-opacity="0.8"'))
    out.append(f'<g transform="translate(42,355)" stroke="{RED}" stroke-width="2.4" stroke-linecap="round">'
               '<path d="M2,2 L14,14 M14,2 L2,14"/></g>')
    out.append(t("Unknown device", "inter-sb", 12, 66, 364, INK))
    out.append(t("no valid certificate", "inter-m", 10.5, 66, 381, SUB))
    out.append('<path id="atk" d="M200,368 H330 V288" fill="none" stroke="#3A1A1F" stroke-dasharray="4 4"/>')
    out.append('<path id="alert" d="M410,288 V358 H470" fill="none" stroke="#3A2E14" stroke-dasharray="4 4"/>')

    # blocked burst + label
    a0 = 3.0
    out.append(f'<circle cx="330" cy="288" r="5" fill="none" stroke="{RED}" stroke-width="2" opacity="0">'
               f'<animate attributeName="opacity" {window(a0, a0 + 0.9, 0.02)}/>'
               f'<animate attributeName="r" values="5;5;26;26" keyTimes="0;{a0 / CYCLE:.4f};{(a0 + 0.9) / CYCLE:.4f};1" '
               f'dur="{CYCLE}s" repeatCount="indefinite"/></circle>')
    out.append(f'<g opacity="0"><animate attributeName="opacity" {window(a0, 6.0)}/>'
               f'<rect x="216" y="296" width="112" height="18" rx="9" fill="{RED}" fill-opacity="0.15" stroke="{RED}"/>'
               + t("✕ handshake rejected", "mono-b", 9, 272, 309, RED, anchor="middle") + "</g>")

    # ---------------------------------------------------------------- packets
    for i in range(5):
        out.append(loop_packet(f"f{i}", 2.4, i * 0.45))
    out.append(loop_packet("tun", 1.6, 0.2, r=4))
    out.append(loop_packet("tun", 1.6, 1.0, r=4))
    out.append(loop_packet("db", 0.8, 0.5, r=3.2))
    out.append(loop_packet("logs", 1.4, 0.3, color=CYAN, r=2.6))
    out.append(one_shot_motion("atk", 1.9, 3.0, RED, r=5))
    out.append(one_shot_motion("alert", 3.2, 4.0, GOLD, r=4.5))

    body = "\n    ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Vila Aurora architecture: devices with their own certificates send data through an edge node and a WireGuard tunnel to the cloud; an attacker without a certificate is rejected and the SIEM raises an alert">
  <title>Vila Aurora — secure and resilient community network</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070C16"/><stop offset="1" stop-color="#0C1828"/></linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#17212F"/></pattern>
    <filter id="glow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    {body}
    <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#1B2A3D"/>
  </g>
</svg>
'''


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "assets" / "vila-aurora.svg")
    s = build()
    open(out, "w").write(s)
    print(out, len(s), "bytes")
