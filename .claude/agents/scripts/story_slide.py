#!/usr/bin/env python3
"""
Story-Slides für Körperverwandlung rendern, 1080 x 1920.

Baut aus einem Foto und ein paar Textzeilen eine fertige Instagram-Story-Slide:
weiße Kästen, schwarze Schrift, zentriert, dazu optional der
Fragensticker "Stell mir eine Frage".

Benutzung als Modul:

    from story_slide import render_slide

    render_slide(
        photo="foto1.jpg",
        out="slide_01.png",
        sticker="ich bin 54... ist es dafür nicht zu spät?",
        boxes=["Nie zu spät", "Dein Körper reagiert in jedem Alter. 💫"],
        top=0.10,            # wo der Block anfängt, 0.0 oben bis 1.0 unten
        align="center",      # center, left, right
    )

Benutzung von der Kommandozeile:

    python3 story_slide.py --photo foto1.jpg --out slide_01.png \
        --sticker "ich bin 54... ist es dafür nicht zu spät?" \
        --box "Nie zu spät" --box "Dein Körper reagiert in jedem Alter. 💫"

Schriftart: Decor ist Projektvorgabe. Liegt die Datei nicht vor, wird die
nächstliegende geometrische Rundschrift genommen und eine Warnung ausgegeben.
Lege Decor.ttf oder Decor.otf in .claude/agents/fonts/ ab, dann wird sie
automatisch benutzt.
"""

import argparse
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1920

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")

# Reihenfolge der Schriftsuche. Decor zuerst, dann geometrische Rundschriften.
FONT_CANDIDATES = [
    (os.path.join(FONT_DIR, "Decor.ttf"), "Decor"),
    (os.path.join(FONT_DIR, "Decor.otf"), "Decor"),
    (os.path.join(FONT_DIR, "Decor-Regular.ttf"), "Decor"),
    ("/usr/share/fonts/opentype/urw-base35/URWGothic-Book.otf", "URW Gothic"),
    ("/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf", "Open Sans"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVu Sans"),
]

BOLD_CANDIDATES = [
    (os.path.join(FONT_DIR, "Decor-Bold.ttf"), "Decor Bold"),
    (os.path.join(FONT_DIR, "Decor-Bold.otf"), "Decor Bold"),
    ("/usr/share/fonts/opentype/urw-base35/URWGothic-Demi.otf", "URW Gothic Demi"),
    ("/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf", "Open Sans Bold"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVu Sans Bold"),
]

# Der Fragensticker wird von Instagram selbst gesetzt, nicht in Decor. Instagram
# nutzt eine neutrale Grotesk, deshalb hier bewusst eine andere Schrift als für die
# Antwortkästen. Nimbus Sans kommt SF Pro am nächsten.
STICKER_CANDIDATES = [
    ("/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf", "Nimbus Sans Bold"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "Liberation Sans Bold"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVu Sans Bold"),
]

# Maße aus dem Instagram-Original abgemessen, als Anteil der Bildbreite 1080
STICKER_WIDTH = 0.64      # Breite des Fragenstickers
STICKER_RADIUS = 26       # Eckenradius der äußeren Ecken des Stickers
STICKER_HEADER_H = 109    # Höhe des dunklen Kopfbalkens
BOX_RADIUS = 0            # Antwortkästen sind im Original scharfkantig
BOX_PAD_X = 35
BOX_PAD_Y = 38
BOX_LINE_H = 1.15         # Zeilenabstand der Antwortkästen
GAP_STICKER = 70          # Abstand Sticker zu erstem Antwortkasten
GAP_BOX = 24              # Abstand zwischen zwei Antwortkästen

EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
EMOJI_NATIVE = 109  # NotoColorEmoji liefert Bitmaps in dieser Groesse

# Emoji inklusive Hautton-Modifier und Zero-Width-Joiner-Ketten
EMOJI_RE = re.compile(
    "([\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍"
    "\U0001F3FB-\U0001F3FF]+)"
)


def _pick(candidates, label):
    for path, name in candidates:
        if os.path.exists(path):
            if name not in ("Decor", "Decor Bold"):
                print(
                    f"  Hinweis: Schriftart Decor nicht gefunden, {label} wird mit "
                    f"'{name}' gesetzt. Lege Decor in .claude/agents/fonts/ ab.",
                    file=sys.stderr,
                )
            return path, name
    raise RuntimeError("Keine brauchbare Schriftdatei gefunden.")


_REG_PATH, REG_NAME = _pick(FONT_CANDIDATES, "Fliesstext")
_BOLD_PATH, BOLD_NAME = _pick(BOLD_CANDIDATES, "Fettschrift")
_STICKER_PATH = next(p for p, _ in STICKER_CANDIDATES if os.path.exists(p))


def font(size, bold=False):
    return ImageFont.truetype(_BOLD_PATH if bold else _REG_PATH, size)


def sticker_font(size):
    """Schrift des Fragenstickers. Instagram setzt ihn selbst, nicht in Decor."""
    return ImageFont.truetype(_STICKER_PATH, size)


def _emoji_img(char, size):
    """Ein Farb-Emoji als RGBA-Bild in der gewuenschten Hoehe."""
    if not os.path.exists(EMOJI_FONT):
        return None
    try:
        f = ImageFont.truetype(EMOJI_FONT, EMOJI_NATIVE)
        tmp = Image.new("RGBA", (EMOJI_NATIVE + 40, EMOJI_NATIVE + 40), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((20, 20), char, font=f, embedded_color=True)
        bbox = tmp.getbbox()
        if not bbox:
            return None
        tmp = tmp.crop(bbox)
        scale = size / tmp.height
        return tmp.resize(
            (max(1, int(tmp.width * scale)), max(1, int(tmp.height * scale))),
            Image.LANCZOS,
        )
    except Exception:
        return None


def _split(text):
    """Text in Stuecke aus Klartext und Emoji zerlegen."""
    return [(p, bool(EMOJI_RE.fullmatch(p))) for p in EMOJI_RE.split(text) if p]


def _measure(draw, text, f):
    """Breite und Hoehe einer Zeile, Emojis mitgerechnet."""
    width = 0
    em = f.size
    for part, is_emoji in _split(text):
        if is_emoji:
            img = _emoji_img(part, em)
            width += (img.width + int(em * 0.10)) if img else 0
        else:
            width += draw.textlength(part, font=f)
    asc, desc = f.getmetrics()
    return width, asc + desc


def _draw_line(base, draw, xy, text, f, fill):
    """Eine Zeile zeichnen, Emojis als Bild eingesetzt."""
    x, y = xy
    asc, _ = f.getmetrics()
    em = f.size
    for part, is_emoji in _split(text):
        if is_emoji:
            img = _emoji_img(part, em)
            if img:
                base.paste(img, (int(x), int(y + asc - img.height * 0.88)), img)
                x += img.width + int(em * 0.10)
        else:
            draw.text((x, y), part, font=f, fill=fill)
            x += draw.textlength(part, font=f)


def _wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if _measure(draw, trial, f)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _cover(photo_path, crop_x=0, crop_y=0):
    """
    Foto auf 1080 x 1920 bringen, ohne Verzerrung.

    crop_x verschiebt den Ausschnitt waagerecht, crop_y senkrecht, jeweils in
    Pixeln. Negativ heißt, es wird mehr vom linken beziehungsweise oberen Rand
    behalten. Nötig, wenn das Gesicht am Bildrand sitzt und der mittige
    Beschnitt es anschneiden würde.
    """
    img = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS)
    left = max(0, min(img.width - W, (img.width - W) // 2 + int(crop_x)))
    top = max(0, min(img.height - H, (img.height - H) // 2 + int(crop_y)))
    return img.crop((left, top, left + W, top + H))


def _text_block(base, draw, text, f, box_w, pad_x, pad_y):
    """Masse eines Antwortkastens. Gibt Zeilen, Breite, Hoehe und Zeilenabstand."""
    lines = _wrap(draw, text, f, box_w - 2 * pad_x)
    lh = int(f.size * BOX_LINE_H)
    inner_w = max(_measure(draw, l, f)[0] for l in lines)
    w = int(inner_w + 2 * pad_x)
    h = int((len(lines) - 1) * lh + f.size * 1.02 + 2 * pad_y)
    return lines, w, h, lh


def _draw_sticker(base, draw, x, y, width, title, frage):
    """
    Fragensticker wie in der Instagram App: dunkler Kopfbalken oben, weisses
    Fragefeld darunter, beides eine Einheit. Nur die aeusseren Ecken sind
    gerundet, die Nahtstelle in der Mitte ist gerade.
    """
    f_title = sticker_font(int(width * 0.044))
    f_q = sticker_font(int(width * 0.068))

    pad_x = int(width * 0.06)
    q_lines = _wrap(draw, frage, f_q, width - 2 * pad_x)
    q_lh = int(f_q.size * 1.30)
    q_h = int((len(q_lines) - 1) * q_lh + f_q.size * 1.02 + 2 * 46)
    header_h = STICKER_HEADER_H
    total_h = header_h + q_h
    r = STICKER_RADIUS

    # Gesamtflaeche weiss, danach der dunkle Kopf darueber. Der Kopf bekommt
    # oben die Rundung und unten eine gerade Kante, damit die Naht sauber ist.
    draw.rounded_rectangle([x, y, x + width, y + total_h], radius=r, fill=(255, 255, 255))
    draw.rounded_rectangle([x, y, x + width, y + header_h], radius=r, fill=(38, 38, 38))
    draw.rectangle([x, y + header_h - r, x + width, y + header_h], fill=(38, 38, 38))

    tw = _measure(draw, title, f_title)[0]
    _draw_line(
        base, draw,
        (x + (width - tw) / 2, y + (header_h - f_title.size * 1.15) / 2),
        title, f_title, (255, 255, 255),
    )

    ly = y + header_h + 46
    for line in q_lines:
        lw = _measure(draw, line, f_q)[0]
        _draw_line(base, draw, (x + (width - lw) / 2, ly), line, f_q, (0, 0, 0))
        ly += q_lh

    return total_h


def render_slide(
    photo,
    out,
    boxes,
    sticker=None,
    sticker_title="Stell mir eine Frage",
    top=0.10,
    align="center",
    box_size=52,
    first_box_size=None,
    gap=GAP_BOX,
    max_width=0.86,
    sticker_width=STICKER_WIDTH,
    crop_x=0,
    crop_y=0,
):
    """
    photo            Pfad zum Hintergrundfoto
    out              Zielpfad der PNG-Datei
    boxes            Liste der Antwortkaesten, je ein String
    sticker          Text im Fragensticker, None wenn kein Sticker
    top              Startpunkt des Blocks als Anteil der Bildhoehe
    box_size         Schriftgroesse der Antwortkaesten
    first_box_size   Abweichende Groesse fuer Kasten 1, sonst wie box_size
    sticker_width    Breite des Fragenstickers als Anteil der Bildbreite
    crop_x, crop_y   Verschiebung des Bildausschnitts in Pixeln
    """
    base = _cover(photo, crop_x, crop_y)
    draw = ImageDraw.Draw(base)

    avail = int(W * max_width)
    margin = (W - avail) // 2
    y = int(H * top)

    if sticker:
        sw = int(W * sticker_width)
        if align == "left":
            sx = 40
        elif align == "right":
            sx = W - 40 - sw
        else:
            sx = (W - sw) // 2
        # Der Sticker hat seine eigene Breite und darf breiter sein als die
        # Textspalte. Begrenzt wird er am Bildrand, nicht an der Spalte.
        rand = 40
        sx = max(rand, min(sx, W - rand - sw))
        y += _draw_sticker(base, draw, sx, y, sw, sticker_title, sticker) + GAP_STICKER

    for i, text in enumerate(boxes):
        size = first_box_size if (i == 0 and first_box_size) else box_size
        f = font(size)
        pad_x, pad_y, radius = BOX_PAD_X, BOX_PAD_Y, BOX_RADIUS

        lines, bw, bh, lh = _text_block(base, draw, text, f, avail, pad_x, pad_y)

        # Wie beim Sticker am Bildrand ausrichten, nicht an der Textspalte.
        # max_width steuert nur den Umbruch, nicht die Position.
        if align == "left":
            bx = 40
        elif align == "right":
            bx = W - 40 - bw
        else:
            bx = (W - bw) // 2

        draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=radius, fill=(255, 255, 255))
        ly = y + pad_y
        for line in lines:
            lw = _measure(draw, line, f)[0]
            _draw_line(base, draw, (bx + (bw - lw) / 2, ly), line, f, (0, 0, 0))
            ly += lh
        y += bh + gap

    if y > H:
        print(
            f"  Warnung: Der Textblock in {os.path.basename(out)} laeuft unten aus dem "
            f"Bild ({y} von {H} px). Kuerze den Text oder setze top kleiner.",
            file=sys.stderr,
        )

    base.save(out, "PNG")
    return out


def main():
    p = argparse.ArgumentParser(description="Story-Slide rendern, 1080x1920")
    p.add_argument("--photo", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--sticker", default=None)
    p.add_argument("--box", action="append", default=[])
    p.add_argument("--top", type=float, default=0.10)
    p.add_argument("--align", default="center", choices=["center", "left", "right"])
    p.add_argument("--box-size", type=int, default=58)
    a = p.parse_args()
    render_slide(
        photo=a.photo, out=a.out, boxes=a.box, sticker=a.sticker,
        top=a.top, align=a.align, box_size=a.box_size,
    )
    print(a.out)


if __name__ == "__main__":
    main()
