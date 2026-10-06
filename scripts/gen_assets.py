#!/usr/bin/env python3
"""Generate the profile artwork in assets/: hero banner, project cards and stack row.

Every SVG follows the viewer's light/dark preference. Edit the data below and run
`python3 scripts/gen_assets.py` to regenerate.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

MONO = 'ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace'
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'

# --- data -----------------------------------------------------------------

LOGO = [
    " ██████╗ ██╗   ██╗",
    "██╔═══██╗██║   ██║",
    "██║   ██║██║   ██║",
    "██║   ██║╚██╗ ██╔╝",
    "╚██████╔╝ ╚████╔╝ ",
    " ╚═════╝   ╚═══╝  ",
]

INFO = [
    ("name", "wiktor"),
    ("age", "16"),
    ("based", "warsaw, pl"),
    ("focus", "systems · fullstack · ai"),
    ("lang", "rust  python  kotlin  typescript"),
    ("shipping", "corestate"),
    ("cooking", "oversync"),
    ("hobby", "hackintosh EFIs on amd ryzen"),
]

MOTTO = "low-level systems ∩ applied intelligence"

PROJECTS = {
    "corestate": dict(
        desc=["enterprise android backup system: kernelsu-next module,",
              "rust file daemon and an ml optimizer backend across 9 microservices"],
        tags=["rust", "kotlin", "python", "kernelsu"],
        status="shipping", wide=True),
    "oversync": dict(desc=["still under wraps.", "check back soon."],
                     tags=["wip"], status="cooking"),
    "over-hackintosh": dict(desc=["opencore EFI for amd ryzen", "desktops"],
                            tags=["opencore", "acpi"], status="ongoing"),
}

STACK = [
    ("rust", "#dea584"), ("python", "#3572a5"), ("kotlin", "#a97bff"), ("typescript", "#3178c6"),
    ("linux", "#e3b341"), ("pytorch", "#ee4c2c"), ("postgresql", "#336791"), ("redis", "#dc382d"),
    ("neondb", "#00e599"),
]

# --- shared theme ----------------------------------------------------------

THEME = """
:root { --bg:#0d1117; --panel:#161b22; --border:#30363d; --fg:#e6edf3; --dim:#8b949e; --faint:#6e7681;
        --accent:#7ee787; --accent2:#79c0ff; --warm:#ffa657; --pill:#21262d; }
@media (prefers-color-scheme: light) {
  :root { --bg:#ffffff; --panel:#f6f8fa; --border:#d0d7de; --fg:#1f2328; --dim:#59636e; --faint:#818b98;
          --accent:#1a7f37; --accent2:#0969da; --warm:#bc4c00; --pill:#eaeef2; }
}
.mono { font-family: %s; }
.sans { font-family: %s; }
""" % (MONO, SANS)


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>{THEME}{css}</style>{body}</svg>\n')


def fade(begin, dur=0.3):
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
            f'dur="{dur}s" fill="freeze"/>')


# --- hero: neofetch-style terminal ------------------------------------------

def hero():
    W, FONT, LH = 900, 14, 22
    cw = FONT * 0.6
    left, top = 40, 68
    info_x = 330

    cmd = "neofetch"
    t0 = 0.4
    type_dur = len(cmd) * 0.07
    reveal = t0 + type_dur + 0.25

    parts = []

    # typed command
    n = len(cmd) + 2
    vals = ";".join(f"{k * cw:.1f}" for k in range(n + 1))
    parts.append(f'<clipPath id="type"><rect x="{left}" y="{top - 16}" width="0" height="24">'
                 f'<animate attributeName="width" begin="{t0}s" dur="{type_dur:.2f}s" calcMode="discrete" '
                 f'values="{vals}" fill="freeze"/></rect></clipPath>')
    parts.append(f'<text class="mono" x="{left}" y="{top}" clip-path="url(#type)">'
                 f'<tspan class="prompt">❯</tspan> <tspan class="cmd">{cmd}</tspan></text>')

    # logo: pixel art built from the solid cells of LOGO, with a drop shadow
    cell_w, cell_h = 13, 19
    logo_y = top + 36 + (len(INFO) + 3) * LH / 2 - len(LOGO) * cell_h / 2 - 8
    lw, lh = len(LOGO[0]) * cell_w, len(LOGO) * cell_h
    parts.append(f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{left}" y1="{logo_y:.1f}" '
                 f'x2="{left + lw}" y2="{logo_y + lh:.1f}">'
                 '<stop offset="0" class="g1"/><stop offset="1" class="g2"/></linearGradient>')
    cells = [(c, r) for r, line in enumerate(LOGO) for c, ch in enumerate(line) if ch == "█"]
    shadow = "".join(f'<rect x="{left + c * cell_w + 4}" y="{logo_y + r * cell_h + 4:.1f}" '
                     f'width="{cell_w}" height="{cell_h}"/>' for c, r in cells)
    solid = "".join(f'<rect x="{left + c * cell_w}" y="{logo_y + r * cell_h:.1f}" '
                    f'width="{cell_w + 0.5}" height="{cell_h + 0.5}"/>' for c, r in cells)
    parts.append(f'<g opacity="0">{fade(reveal, 0.5)}<g class="shadow">{shadow}</g>'
                 f'<g fill="url(#g)">{solid}</g></g>')

    # info column
    y = top + 36
    head = "overspend1@warsaw"
    items = ['<tspan class="user">overspend1</tspan><tspan class="dim">@</tspan><tspan class="user">warsaw</tspan>',
             f'<tspan class="faint">{"─" * len(head)}</tspan>']
    items += [f'<tspan class="key">{k:<10}</tspan><tspan class="val">{escape(v)}</tspan>' for k, v in INFO]
    for i, content in enumerate(items):
        parts.append(f'<text class="mono" x="{info_x}" y="{y}" opacity="0">{content}'
                     f'{fade(reveal + 0.15 + i * 0.07, 0.25)}</text>')
        y += LH

    # colour blocks
    d = reveal + 0.15 + len(items) * 0.07
    blocks = ["#ff7b72", "#ffa657", "#e3b341", "#7ee787", "#79c0ff", "#d2a8ff", "#f778ba", "#8b949e"]
    parts.append(f'<g opacity="0">{fade(d)}' + "".join(
        f'<rect x="{info_x + i * 26}" y="{y - 8}" width="22" height="12" rx="3" fill="{c}"/>'
        for i, c in enumerate(blocks)) + "</g>")

    # motto line with blinking cursor
    y += LH * 1.7
    d += 0.35
    parts.append(f'<g opacity="0">{fade(d)}'
                 f'<text class="mono" x="{left}" y="{y:.1f}"><tspan class="prompt">❯</tspan> '
                 f'<tspan class="faint"># </tspan><tspan class="motto">{escape(MOTTO)}</tspan></text>'
                 f'<rect class="cursor" x="{left + (len(MOTTO) + 5) * cw:.1f}" y="{y - 12:.1f}" '
                 f'width="{cw:.1f}" height="16"/></g>')

    H = int(y + 34)
    chrome = [f'<rect class="win" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12"/>',
              f'<path class="bar" d="M12.5 .5h{W - 25}a12 12 0 0 1 12 12v24h-{W - 1}v-24a12 12 0 0 1 12-12z"/>',
              f'<line class="sep" x1="0.5" y1="36.5" x2="{W - 0.5}" y2="36.5"/>']
    chrome += [f'<circle cx="{22 + i * 20}" cy="18.5" r="6" fill="{c}"/>'
               for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))]
    chrome.append(f'<text class="mono title" x="{W / 2}" y="23" text-anchor="middle">overspend1@warsaw: ~</text>')

    css = f"""
    text {{ font-size:{FONT}px; fill:var(--fg); white-space:pre; }}
    .win {{ fill:var(--bg); stroke:var(--border); }} .bar {{ fill:var(--panel); }} .sep {{ stroke:var(--border); }}
    .title {{ font-size:12px; fill:var(--dim); }}
    .prompt {{ fill:var(--accent); font-weight:700; }} .cmd {{ font-weight:600; }}
    .shadow {{ fill:var(--border); }}
    .g1 {{ stop-color:#7ee787; }} .g2 {{ stop-color:#79c0ff; }}
    @media (prefers-color-scheme: light) {{ .g1 {{ stop-color:#1a7f37; }} .g2 {{ stop-color:#0969da; }} }}
    .user {{ fill:var(--accent2); font-weight:700; }} .dim {{ fill:var(--dim); }} .faint {{ fill:var(--faint); }}
    .key {{ fill:var(--accent); font-weight:700; }} .val {{ fill:var(--fg); }}
    .motto {{ fill:var(--warm); }}
    .cursor {{ fill:var(--accent); animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity:0; }} }}
    """
    return svg(W, H, "".join(chrome + parts), css, "neofetch: wiktor, 16, warsaw, systems, fullstack and ai")


# --- project cards ------------------------------------------------------------

STATUS = {"shipping": "#3fb950", "cooking": "#d29922", "ongoing": "#58a6ff"}
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 "
             "0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 "
             "1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 "
             "0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z")


def card(name, p):
    W = 900 if p.get("wide") else 444
    H = 150
    color = STATUS[p["status"]]
    parts = [f'<clipPath id="r"><rect x="0" y="0" width="{W}" height="{H}" rx="12"/></clipPath>',
             f'<rect class="card" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12"/>',
             f'<rect x="0" y="0" width="4" height="{H}" fill="{color}" clip-path="url(#r)"/>',
             f'<path class="icon" transform="translate(24 21)" d="{REPO_ICON}"/>',
             f'<text class="sans name" x="48" y="35">{escape(name)}</text>']

    label = p["status"]
    pw = 30 + len(label) * 7.3
    px = W - 20 - pw
    parts.append(f'<rect class="pill" x="{px:.1f}" y="19" width="{pw:.1f}" height="24" rx="12"/>'
                 f'<circle cx="{px + 13:.1f}" cy="31" r="4" fill="{color}">'
                 f'<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>'
                 f'<text class="mono status" x="{px + 23:.1f}" y="35">{label}</text>')
    for i, line in enumerate(p["desc"]):
        parts.append(f'<text class="sans desc" x="24" y="{72 + i * 21}">{escape(line)}</text>')
    x = 24
    for t in p["tags"]:
        tw = 18 + len(t) * 7.3
        parts.append(f'<rect class="tag" x="{x:.1f}" y="{H - 40}" width="{tw:.1f}" height="22" rx="11"/>'
                     f'<text class="mono tagt" x="{x + tw / 2:.1f}" y="{H - 25}" text-anchor="middle">{t}</text>')
        x += tw + 8
    css = """
    .card { fill:var(--bg); stroke:var(--border); }
    .icon { fill:var(--dim); }
    .name { font-size:18px; font-weight:600; fill:var(--accent2); }
    .desc { font-size:14px; fill:var(--dim); }
    .pill { fill:var(--pill); } .status { font-size:12px; fill:var(--fg); }
    .tag { fill:none; stroke:var(--border); } .tagt { font-size:12px; fill:var(--dim); }
    """
    return svg(W, H, "".join(parts), css, f"{name}: {' '.join(p['desc'])}")


# --- stack row -----------------------------------------------------------------

def stack():
    W, H = 900, 44
    widths = [34 + len(n) * 7.8 for n, _ in STACK]
    gap = (W - 2 - sum(widths)) / (len(STACK) - 1)
    parts, x = [], 1.0
    for (n, c), w in zip(STACK, widths):
        parts.append(f'<rect class="chip" x="{x:.1f}" y="6" width="{w:.1f}" height="32" rx="16"/>'
                     f'<circle cx="{x + 16:.1f}" cy="22" r="5" fill="{c}"/>'
                     f'<text class="mono chipt" x="{x + 27:.1f}" y="26.5">{n}</text>')
        x += w + gap
    css = """
    .chip { fill:var(--panel); stroke:var(--border); }
    .chipt { font-size:13px; fill:var(--fg); }
    """
    return svg(W, H, "".join(parts), css, "stack: " + ", ".join(n for n, _ in STACK))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(), "stack.svg": stack()}
    for name, p in PROJECTS.items():
        files[f"card-{name}.svg"] = card(name, p)
    for f, content in files.items():
        (OUT / f).write_text(content, encoding="utf-8")
        print("wrote", OUT / f)
