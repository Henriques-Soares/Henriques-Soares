"""Convert text to SVG path data with fontTools, so the SVG renders the same everywhere."""
from functools import lru_cache

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = {
    "display-xb": "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf",
    "display-b": "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "inter-sb": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "inter-m": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "mono-b": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}


@lru_cache(maxsize=None)
def _font(name):
    f = TTFont(FONTS[name])
    return f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm


def text_width(text, font, size, spacing=0.0):
    _, _, cmap, hmtx, upem = _font(font)
    w = 0.0
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        w += hmtx[g][0] * size / upem + spacing
    return w - (spacing if text else 0)


def text_path(text, font, size, x, y, spacing=0.0, anchor="start"):
    """Return SVG path 'd' for text with baseline at y."""
    _, gs, cmap, hmtx, upem = _font(font)
    scale = size / upem
    if anchor == "middle":
        x -= text_width(text, font, size, spacing) / 2
    elif anchor == "end":
        x -= text_width(text, font, size, spacing)
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cx = x
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[g].draw(tp)
        cx += hmtx[g][0] * scale + spacing
    return pen.getCommands()


def mono_advance(size, font="mono"):
    _, _, cmap, hmtx, upem = _font(font)
    return hmtx[cmap[ord("M")]][0] * size / upem
