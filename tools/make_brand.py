#!/usr/bin/env python3
"""Generates the StoneBuild Games logo package (brand/) and the website icons (site/).
Run from the repo root: python3 tools/make_brand.py"""
import os, zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ORANGE, DEEP = "#FF6A2B", "#9E411A"
GEOM = dict(
    top="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60",
    right="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80",
    left="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140",
    floor="100,100 134.64,120 100,140 65.36,120",
    wall_l="100,60 100,100 65.36,120 65.36,80",
    wall_r="100,60 134.64,80 134.64,120 100,100",
    p_top="172,14 185.86,22 172,30 158.14,22",
    p_right="172,30 185.86,22 185.86,38 172,46",
    p_left="158.14,22 172,30 172,46 158.14,38",
)
ON_DARK = dict(top=ORANGE, right="#8B8B95", left="#FFFFFF", floor=DEEP, wall_l="#55555E", wall_r="#D4D4D8", p_top=ORANGE, p_right="#8B8B95", p_left="#FFFFFF")
ON_LIGHT = dict(top=ORANGE, right="#52525B", left="#0A0A0B", floor=DEEP, wall_l="#27272A", wall_r="#3F3F46", p_top=ORANGE, p_right="#52525B", p_left="#0A0A0B")
ORDER = list(GEOM)
VB = (18, 7, 180, 180)

def polys_svg(c, stroke, sw=3):
    p = "".join(f'<polygon points="{GEOM[k]}" fill="{c[k]}"/>' for k in ORDER)
    return f'<g stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{p}</g>'

def mark_svg(c, stroke):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 7 180 180" role="img" aria-label="StoneBuild Games logo">{polys_svg(c, stroke)}</svg>\n'

def text_path(font_path, text, size, x, y, tracking, fill):
    """Text converted to outlines so the SVG needs no font installed. Returns (svg, end_x)."""
    font = TTFont(font_path); gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm; s = size / upm
    out = []; cx = x
    for ch in text:
        g = cmap.get(ord(ch)); glyph = gs[g]
        pen = SVGPathPen(gs); glyph.draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        d = pen.getCommands()
        if d: out.append(f'<path d="{d}"/>')
        cx += glyph.width * s + tracking * size
    return f'<g fill="{fill}">{"".join(out)}</g>', cx - tracking * size

CHAKRA, MONO = "tools/fonts/ChakraPetch-Bold.ttf", "tools/fonts/JetBrainsMono-Medium.ttf"

def lockup_svg(c, stroke, ink, sub):
    # Proportions from the supplied concept: 72px mark, 20px gap, 34px name, 13px spaced GAMES
    t1, end = text_path(CHAKRA, "STONE BUILD", 34, 92, 38, 0.02, ink)
    t2, _ = text_path(MONO, "GAMES", 13, 92, 60, 0.62, sub)
    W = round(end + 2)
    mark = f'<svg x="0" y="0" width="72" height="72" viewBox="18 7 180 180">{polys_svg(c, stroke)}</svg>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 72" role="img" aria-label="StoneBuild Games">{mark}{t1}{t2}</svg>\n', W

def app_icon_svg(bg="#0E0E10", rounded=False):
    k = 330 / 180  # mark occupies the store safe zone (about 64%)
    corner = ' rx="96"' if rounded else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512"{corner} fill="{bg}"/>'
            f'<g transform="translate(91 91) scale({k:.4f}) translate(-18 -7)">{polys_svg(ON_DARK, bg)}</g></svg>\n')

BLOCK = ['top', 'right', 'left', 'floor', 'wall_l', 'wall_r']  # the small cube is unreadable at favicon size
def favicon_svg():
    p = "".join(f'<polygon points="{GEOM[k]}" fill="{ON_LIGHT[k]}"/>' for k in BLOCK)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="14 14 172 172"><g stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round">{p}</g></svg>\n'
def draw_favicon(size, ss=8):
    W = size * ss; k = W / 172
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); sw = max(1, round(5 * k))
    for key in BLOCK:
        q = [((float(a) - 14) * k, (float(b) - 14) * k) for a, b in (x.split(',') for x in GEOM[key].split())]
        d.polygon(q, fill=ON_LIGHT[key]); d.line(q + [q[0]], fill="#FFFFFF", width=sw, joint="curve")
    return im.resize((size, size), Image.LANCZOS)
def white_icon(size):
    im = Image.new("RGBA", (size, size), "#FFFFFF"); m = round(size * .8)
    im.alpha_composite(draw_favicon(m), ((size - m) // 2, (size - m) // 2)); return im.convert("RGB")

def hex2(c): return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))

def draw_mark(size, c, stroke, ss=4):
    W = size * ss; k = W / 180
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); sw = max(1, round(3 * k))
    for key in ORDER:
        p = [((float(a) - 18) * k, (float(b) - 7) * k) for a, b in (q.split(',') for q in GEOM[key].split())]
        d.polygon(p, fill=c[key]); d.line(p + [p[0]], fill=stroke, width=sw, joint="curve")
    return im.resize((size, size), Image.LANCZOS)

def draw_text(im, font_path, text, size, xy, tracking, fill, ss=4):
    f = ImageFont.truetype(font_path, size * ss); W, H = im.size
    layer = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(layer); x = xy[0] * ss
    asc, _ = f.getmetrics(); y = (xy[1]) * ss - asc  # xy is the baseline
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + tracking * size * ss
    im.alpha_composite(layer.resize((W, H), Image.LANCZOS))

def draw_lockup(width, c, stroke, ink, sub, svg_w, bg=None):
    k = width / svg_w; H = round(72 * k)
    im = Image.new("RGBA", (width, H), bg or (0, 0, 0, 0))
    im.alpha_composite(draw_mark(H, c, stroke), (0, 0))
    draw_text(im, CHAKRA, "STONE BUILD", round(34 * k), (round(92 * k), round(38 * k)), 0.02, ink)
    draw_text(im, MONO, "GAMES", round(13 * k), (round(92 * k), round(60 * k)), 0.62, sub)
    return im

def app_icon_png(size, bg="#0E0E10"):
    im = Image.new("RGBA", (size, size), bg); m = round(size * 330 / 512)
    im.alpha_composite(draw_mark(m, ON_DARK, bg), ((size - m) // 2, (size - m) // 2)); return im

def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w").write(data)

def glow(W, H, spots):
    g = Image.new("RGB", (W, H), "#FFFFFF"); d = ImageDraw.Draw(g)
    for box, col in spots: d.ellipse(box, fill=col)
    return g.filter(ImageFilter.GaussianBlur(120)).convert("RGBA")

def main():
    # ---------- SVG ----------
    write("brand/svg/mark-for-light-background.svg", mark_svg(ON_LIGHT, "#FFFFFF"))
    write("brand/svg/mark-for-dark-background.svg", mark_svg(ON_DARK, "#000000"))
    l_light, W = lockup_svg(ON_LIGHT, "#FFFFFF", "#0A0A0B", "#C7430F")
    l_dark, _ = lockup_svg(ON_DARK, "#000000", "#FFFFFF", ORANGE)
    write("brand/svg/logo-for-light-background.svg", l_light)
    write("brand/svg/logo-for-dark-background.svg", l_dark)
    write("brand/svg/app-icon.svg", app_icon_svg())
    # ---------- PNG ----------
    os.makedirs("brand/png", exist_ok=True)
    draw_mark(1024, ON_LIGHT, "#FFFFFF").save("brand/png/mark-for-light-background-1024.png", optimize=True)
    draw_mark(1024, ON_DARK, "#000000").save("brand/png/mark-for-dark-background-1024.png", optimize=True)
    draw_lockup(2000, ON_LIGHT, "#FFFFFF", "#0A0A0B", "#C7430F", W).save("brand/png/logo-for-light-background-2000.png", optimize=True)
    draw_lockup(2000, ON_DARK, "#000000", "#FFFFFF", ORANGE, W).save("brand/png/logo-for-dark-background-2000.png", optimize=True)
    app_icon_png(1024).convert("RGB").save("brand/png/app-icon-1024.png", optimize=True)
    app_icon_png(512).convert("RGB").save("brand/png/google-play-icon-512.png", optimize=True)
    # Play Store feature graphic 1024x500
    fg = glow(1024, 500, [((560, -260, 1240, 360), "#FFE3D4")])
    fg.alpha_composite(draw_mark(360, ON_LIGHT, "#FFFFFF"), (620, 70))
    fg.alpha_composite(draw_lockup(470, ON_LIGHT, "#FFFFFF", "#0A0A0B", "#C7430F", W), (70, 190))
    fg.convert("RGB").save("brand/png/google-play-feature-graphic-1024x500.png", optimize=True)
    # ---------- Website icons ----------
    if os.path.isdir("site/assets"):
        write("site/assets/favicon.svg", favicon_svg())
        write("site/assets/logo.svg", l_light)
        draw_favicon(48).save("site/assets/favicon-48.png", optimize=True)
        white_icon(512).save("site/assets/logo-512.png", optimize=True)
        white_icon(192).save("site/assets/icon-192.png", optimize=True)
        white_icon(180).save("site/assets/apple-touch-icon.png", optimize=True)
        draw_favicon(256).save("site/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        # Social share image, white theme
        og = glow(1200, 630, [((640, -360, 1400, 400), "#FFDCC9")])
        og.alpha_composite(draw_lockup(380, ON_LIGHT, "#FFFFFF", "#0A0A0B", "#C7430F", W), (96, 84))
        draw_text(og, CHAKRA, "Building worlds", 70, (96, 340), -0.01, "#0A0A0B")
        draw_text(og, CHAKRA, "worth playing.", 70, (96, 424), -0.01, "#F2570F")
        draw_text(og, MONO, "GAME DEVELOPMENT STUDIO", 20, (96, 492), 0.12, "#52525B")
        draw_text(og, MONO, "STONEBUILDGAMES.COM", 20, (96, 528), 0.12, "#71717A")
        og.alpha_composite(draw_mark(360, ON_LIGHT, "#FFFFFF"), (790, 130))
        og.convert("RGB").save("site/assets/og-image.png", optimize=True)
    # ---------- Zip for easy download ----------
    with zipfile.ZipFile("brand/StoneBuild-Games-logo-package.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for sub in ("svg", "png"):
            for fn in sorted(os.listdir(f"brand/{sub}")):
                z.write(f"brand/{sub}/{fn}", f"StoneBuild-Games-logo/{sub}/{fn}")
    print("brand package ok")

if __name__ == "__main__":
    main()
