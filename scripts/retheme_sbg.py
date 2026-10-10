"""Re-theme slides/visuals/*.svg to the AWS Student Builder Group Canva template.

Template (Canva PDF, 2026-09-29): dark #161d26 with a 60 px grid, flat pixel blocks in
orange / purple / magenta / blue / green, IBM Plex Mono headlines, Public Sans body.
Writes slides/visuals-sbg/<same name>.svg; the light originals stay untouched.

  python3 scripts/retheme_sbg.py
"""
import pathlib
import random
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent / "slides"
SRC, OUT = ROOT / "visuals", ROOT / "visuals-sbg"

BG, CARD, GRID = "#161d26", "#1f2731", "#3e434c"
ORANGE, PURPLE, MAGENTA, BLUE, GREEN = "#ff9900", "#ad5cff", "#ff57e9", "#42b4ff", "#00e582"
BLOCKS = [ORANGE, PURPLE, MAGENTA, BLUE, GREEN]

FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700"
         "&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=block');")
MONO = "'IBM Plex Mono',Menlo,ui-monospace,monospace"
GRID_DEF = (f'<pattern id="sbg-grid" width="60" height="60" patternUnits="userSpaceOnUse">'
            f'<path d="M60 0V60H0" fill="none" stroke="{GRID}" stroke-width="2"/></pattern>')
GRAD3 = ('<stop offset="0" stop-color="#1f6fe5"/><stop offset=".5" stop-color="#7c3aed"/>'
         '<stop offset="1" stop-color="#c026d3"/>')

# Divider page colours, in template rotation (dark text on all of them).
DIVIDERS = {"10a": MAGENTA, "10b": ORANGE, "10c": BLUE, "10d": GREEN, "10e": PURPLE, "10f": MAGENTA, "10g": GREEN}


def mosaic(x0, y0, cols, rows, seed, fill=.5, blink=True):
    """Pixel blocks on the 60 px grid, like the template cover. A few cells blink (8 s loop)."""
    rnd = random.Random(seed)
    cells = []
    for r in range(rows):
        for c in range(cols):
            if rnd.random() < fill:
                cls = ' class="blink"' if blink and rnd.random() < .12 else ""
                d = f' style="animation-delay:-{rnd.randint(0, 7)}s"' if cls else ""
                cells.append(f'<rect x="{x0 + c * 60}" y="{y0 + r * 60}" width="60" height="60" '
                             f'fill="{rnd.choice(BLOCKS)}"{cls}{d}/>')
    return "<g>" + "".join(cells) + "</g>"


CORNER = (f'<g><rect x="1800" y="0" width="60" height="60" fill="{ORANGE}"/>'
          f'<rect x="1860" y="0" width="60" height="60" fill="{BLUE}"/>'
          f'<rect x="1860" y="60" width="60" height="60" fill="{MAGENTA}"/></g>')

BLINK_CSS = ("@media (prefers-reduced-motion: no-preference){.blink{animation:blink 8s steps(1) infinite}"
             "@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}}")


def common(s):
    s = re.sub(r"@import url\([^)]*\);", FONTS, s)
    s = s.replace("'Plus Jakarta Sans'", "'Public Sans'").replace("Plus Jakarta Sans", "Public Sans")
    s = s.replace("'JetBrains Mono'", "'IBM Plex Mono'").replace('"JetBrains Mono"', '"IBM Plex Mono"')
    s = s.replace(GRAD3, f'<stop offset="0" stop-color="{ORANGE}"/>')
    s = re.sub(r'flood-opacity="[^"]*"', 'flood-opacity="0"', s)          # flat: no card shadows
    s = re.sub(r'<circle [^>]*url\(#tv-glow-[ab]\)"/>', "", s)
    s = s.replace("</defs>", GRID_DEF + "</defs>", 1)
    return s


def dark(s):
    """Content slides: dark page, grid, light text, orange accent, dark glyphs on orange tiles."""
    s = s.replace('<rect width="1920" height="1080" fill="#fff"/>',
                  '<rect width="1920" height="1080" fill="@GLYPH@"/><rect width="1920" height="1080" fill="url(#sbg-grid)"/>')
    s = s.replace('fill="#161d26" shape-rendering', 'fill="@GLYPH@" shape-rendering')  # QR modules stay dark
    s = s.replace("#FFFFFF", "@GLYPH@")                                  # AWS icon glyphs
    s = re.sub(r"(\.gl \*\{fill:none;stroke:)#fff", r"\1@GLYPH@", s)     # self-drawn glyphs
    s = re.sub(r"(\.(?:card|new|cur)\{fill:)#fff", rf"\1{CARD}", s)
    s = re.sub(r'fill="#fff(?:fff)?"( stroke=)', rf'fill="{CARD}"\1', s)
    for a, b in [("#161d26", "#ffffff"), ("#5b6475", "#b8bec8"), ("#d9dce5", GRID), ("#7c3aed", ORANGE),
                 ("#1f6fe5", BLUE), ("#c026d3", MAGENTA), ("#c4a8ff", PURPLE), ("#f5f6fa", CARD),
                 ("#e6e8ef", CARD), ("#fff4e5", "#2a2418"), ("#d97706", ORANGE), ("#b45309", ORANGE),
                 ("rgb(124 58 237 /", "rgb(255 153 0 /")]:
        s = s.replace(a, b)
    s = s.replace("@GLYPH@", BG)
    s = re.sub(r"\.h\{([^}]*)\}", lambda m: ".h{" + m.group(1) + f";font-family:{MONO};font-weight:500}}", s)
    return s


def title(s, seed, x0=1140):
    """Cover / thank-you: dark page + template mosaic in place of the gradient sweep."""
    s = re.sub(r'<g class="sweep">.*?</g>', mosaic(x0, 0, (1920 - x0) // 60, 16, seed), s, flags=re.S)
    s = s.replace("</style>", BLINK_CSS + "</style>", 1)
    return s


def divider(s, colour, seed):
    s = s.replace('fill="url(#full)"', f'fill="{colour}"/><rect width="1920" height="1080" fill="url(#sbg-grid)" opacity=".35"')
    s = re.sub(r'<g opacity="\.14".*?</g>', mosaic(1380, 0, 9, 18, seed, fill=.35, blink=False), s, flags=re.S)
    s = s.replace(f'stroke="{GRID}"', 'stroke="#161d26"')                # grid lines dark on colour
    s = s.replace('fill="#f5d0fe"', f'fill="{BG}" opacity=".5"').replace('fill="#fff"', f'fill="{BG}"')
    return s


def main():
    OUT.mkdir(exist_ok=True)
    if (SRC / "fotos").exists():
        shutil.copytree(SRC / "fotos", OUT / "fotos", dirs_exist_ok=True)
    for i, f in enumerate(sorted(SRC.glob("*.svg"))):
        s = common(f.read_text())
        key = f.name[:3]
        if key in DIVIDERS:
            s = divider(s, DIVIDERS[key], i)
        else:
            if f.name.startswith(("00-", "00b-")):
                s = title(s, i, 1140 if f.name.startswith("00-") else 1740)
            qr = re.search(r'(<rect x="1180" y="260"[^>]*/>)', s)          # gracias: QR card stays white
            s = re.sub(r'(<text x="1440"[^>]*fill=")#(?:161d26|5b6475)', r"\1@GLYPH@", s)  # QR card captions
            s = dark(s)
            if qr:
                s = re.sub(r'<rect x="1180" y="260"[^>]*/>', qr.group(1), s)
            elif not f.name.startswith(("00-", "03-")):
                s = re.sub(r'(<rect width="1920" height="1080" fill="url\(#sbg-grid\)"/>)', r"\1" + CORNER, s, count=1)
        (OUT / f.name).write_text(s)
        print(OUT / f.name)


if __name__ == "__main__":
    main()
