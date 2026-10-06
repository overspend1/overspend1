#!/usr/bin/env python3
"""Generate assets/terminal.svg: an animated terminal that types out the profile intro.

Edit LINES below and run `python3 scripts/gen_header.py` to regenerate.
"""
from pathlib import Path
from xml.sax.saxutils import escape

W = 860
FONT = 15
CHAR_W = FONT * 0.62  # approximate monospace advance
LINE_H = 26
TOP = 70
LEFT = 28
CHAR_DUR = 0.035  # seconds per typed character
PAUSE = 0.35      # pause after each command line

# (kind, text): "cmd" lines are typed, "out" lines appear at once.
# Segments inside an "out" line can be tinted with [[accent:text]].
LINES = [
    ("cmd", "whoami"),
    ("out", "[[hi:wiktor]]  16 · warsaw · systems, fullstack & ai"),
    ("cmd", "cat ~/now.txt"),
    ("out", "[[hi:corestate]]  android backup · kernelsu module · rust daemon · 9 services"),
    ("out", "[[hi:oversync]]   still cooking"),
    ("cmd", "ls ~/stack"),
    ("out", "[[a1:rust]]  [[a2:python]]  [[a3:kotlin]]  [[a4:typescript]]  [[a5:linux]]  [[a6:pytorch]]"),
    ("cmd", "uptime --motto"),
    ("out", "low-level systems ∩ applied intelligence"),
]


def spans(text):
    out, rest = [], text
    while "[[" in rest:
        pre, _, tail = rest.partition("[[")
        body, _, rest = tail.partition("]]")
        cls, _, word = body.partition(":")
        if pre:
            out.append(f"<tspan>{escape(pre)}</tspan>")
        out.append(f'<tspan class="{cls}">{escape(word)}</tspan>')
    if rest:
        out.append(f"<tspan>{escape(rest)}</tspan>")
    return "".join(out)


def build():
    height = TOP + LINE_H * (len(LINES) + 1) + 10
    defs, body = [], []
    t = 0.6
    y = TOP
    for i, (kind, text) in enumerate(LINES):
        if kind == "cmd":
            n = len(text) + 2
            dur = n * CHAR_DUR
            defs.append(
                f'<clipPath id="c{i}"><rect x="{LEFT}" y="{y - FONT - 2}" width="0" height="{LINE_H}">'
                f'<animate attributeName="width" begin="{t:.2f}s" dur="{dur:.2f}s" '
                f'calcMode="discrete" values="{";".join(f"{k * CHAR_W:.1f}" for k in range(n + 1))}" fill="freeze"/>'
                f"</rect></clipPath>"
            )
            body.append(
                f'<text x="{LEFT}" y="{y}" clip-path="url(#c{i})"><tspan class="p">❯</tspan> '
                f'<tspan class="cmd">{escape(text)}</tspan></text>'
            )
            t += dur + PAUSE
        else:
            body.append(
                f'<text x="{LEFT + 2 * CHAR_W:.1f}" y="{y}" class="out" opacity="0">{spans(text)}'
                f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
            )
            t += 0.12
        y += LINE_H
    # final prompt with blinking cursor
    body.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="{LEFT}" y="{y}"><tspan class="p">❯</tspan></text>'
        f'<rect class="cursor" x="{LEFT + 2 * CHAR_W:.1f}" y="{y - FONT + 2}" width="{CHAR_W:.1f}" height="{FONT + 2}"/></g>'
    )

    css = f"""
    :root {{ --bg:#0d1117; --bar:#161b22; --border:#30363d; --fg:#c9d1d9; --dim:#8b949e;
            --p:#7ee787; --hi:#ffa657; --a1:#f0883e; --a2:#79c0ff; --a3:#d2a8ff; --a4:#58a6ff; --a5:#e3b341; --a6:#ff7b72; }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg:#ffffff; --bar:#f6f8fa; --border:#d0d7de; --fg:#24292f; --dim:#57606a;
              --p:#1a7f37; --hi:#bc4c00; --a1:#bc4c00; --a2:#0969da; --a3:#8250df; --a4:#0550ae; --a5:#9a6700; --a6:#cf222e; }}
    }}
    text {{ font-family: ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, Consolas, monospace;
            font-size:{FONT}px; fill:var(--fg); white-space:pre; }}
    .win {{ fill:var(--bg); stroke:var(--border); }}
    .bar {{ fill:var(--bar); }}
    .title {{ fill:var(--dim); font-size:12px; }}
    .p {{ fill:var(--p); font-weight:700; }}
    .cmd {{ fill:var(--fg); font-weight:600; }}
    .out {{ fill:var(--dim); }}
    .hi {{ fill:var(--hi); font-weight:700; }}
    .a1 {{ fill:var(--a1); }} .a2 {{ fill:var(--a2); }} .a3 {{ fill:var(--a3); }}
    .a4 {{ fill:var(--a4); }} .a5 {{ fill:var(--a5); }} .a6 {{ fill:var(--a6); }}
    .cursor {{ fill:var(--p); animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity:0; }} }}
    """

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="wiktor: 16, warsaw, systems, fullstack and ai">
<style>{css}</style>
<defs>{"".join(defs)}</defs>
<rect class="win" x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" rx="10"/>
<path class="bar" d="M10.5 0.5h{W - 21}a10 10 0 0 1 10 10v24h-{W - 1}v-24a10 10 0 0 1 10-10z"/>
<circle cx="22" cy="18" r="6" fill="#ff5f56"/><circle cx="42" cy="18" r="6" fill="#ffbd2e"/><circle cx="62" cy="18" r="6" fill="#27c93f"/>
<text class="title" x="{W / 2}" y="22" text-anchor="middle">overspend1@warsaw: ~</text>
{chr(10).join(body)}
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out}")
