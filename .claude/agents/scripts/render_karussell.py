#!/usr/bin/env python3
"""
Karussell-Slides für Körperverwandlung rendern, 1080 x 1350 (4:5).

Baut die Hausvorlage aus sabine.md als fertige PNG-Dateien:

    Cover / Schluss (Foto):
        Foto vollflächig, dunkler Verlauf von unten, Badge-Pill, zweizeilige
        Headline (Zeile 1 weiß, Zeile 2 rot), Sub-Zeile mit Pfeil, Logo unten
        links. Die Schluss-Slide bekommt zusätzlich 3 Bullets im selben Stil
        wie die Inhalts-Slides.

    Inhalt (Dunkelblau #0F1D33):
        Badge-Pill oben links, roter Balken, zweizeilige Headline, genau 3
        Bulletpoints mit rotem Icon-Quadrat, große Ziffer als Wasserzeichen,
        Trennlinie, zweizeiliger Abbinder.

Benutzung als Modul:

    import sys
    sys.path.insert(0, ".claude/agents/scripts")
    from render_karussell import render_photo_slide, render_content_slide

    render_photo_slide(
        photo="andreas.jpg",
        out="slide_01.png",
        badge="ERSTER SCHRITT",
        headline=["DIE KÖRPERANALYSE", "VERÄNDERT ALLES"],
        sub="Warum eine Zahl auf der Waage nie die ganze Wahrheit zeigt",
        face_anchor=0.30,   # 0 = Gesicht ganz oben im Ausschnitt, 1 = ganz unten
    )

    render_content_slide(
        out="slide_02.png",
        number="02",
        badge="KÖRPERWERTE",
        headline=["WAS DEINE", "WAAGE VERSCHWEIGT"],
        bullets=[
            ("Muskelmasse", "zeigt, wie viel deines Gewichts wirklich Kraft ist."),
            ("Wasserhaushalt", "erklärt, warum die Zahl täglich schwankt."),
            ("Fettverteilung", "zeigt Veränderung, auch wenn die Waage stillsteht."),
        ],
        outro=("Eine Zahl allein erklärt nie die ganze Geschichte.",
               "Deine Körperanalyse schon."),
    )

Logo: mangels echtem Asset ein Platzhalter, weißes/dunkelblaues K im Kreis
plus KÖRPER (fett) über VERWANDLUNG (leicht), wie in GEMEINSAME-REGELN.md
beschrieben. Sobald ein echtes Logo-Asset vorliegt, ersetzt eine
_draw_logo-Variante mit Image.paste das hier.

Schriftart: font() aus story_slide.py, aktuell Quicksand Medium/Bold,
dieselbe Schrift wie in den Stories.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageOps

from story_slide import font, _measure, _draw_line, _wrap  # noqa: F401  (wiederverwendet)

W, H = 1080, 1350

NAVY = (15, 29, 51)          # #0F1D33
NAVY_WATERMARK = (24, 40, 66)  # etwas heller als der Hintergrund
NAVY_RING = (28, 45, 74)       # Kreislinien, sehr geringer Kontrast
RED = (232, 57, 78)           # #E8394E
WHITE = (255, 255, 255)
GREY = (154, 165, 180)        # #9AA5B4

MARGIN = 72


# --------------------------------------------------------------------------
# Grundbausteine
# --------------------------------------------------------------------------

def _cover(photo_path, focus=0.35, zoom=1.0, crop_x=0):
    """
    Foto auf 1080 x 1350 bringen, ohne Verzerrung.

    focus  Anteil von oben (0.0 bis 1.0), auf den der Ausschnitt zentriert
           werden soll, zum Beispiel 0.3 wenn das Gesicht im oberen Drittel
           des Originalfotos sitzt.
    zoom   zusaetzlicher Zoomfaktor ueber das reine Cover-Fitting hinaus.
           Noetig, wenn das Quellfoto fast im Zielformat ist und sonst kaum
           Spielraum bleibt, eine Geste wie eine hoch gestreckte Hand aus dem
           unteren Bildbereich herauszuschneiden.
    crop_x Verschiebung des Ausschnitts waagerecht in Pixeln, positiv nach
           rechts.
    """
    img = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")
    scale = max(W / img.width, H / img.height) * zoom
    img = img.resize(
        (int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS
    )
    left = max(0, min(img.width - W, (img.width - W) // 2 + int(crop_x)))
    ideal_top = int(img.height * focus) - int(H * focus)
    top = max(0, min(img.height - H, ideal_top))
    return img.crop((left, top, left + W, top + H))


def _gradient_overlay(height_frac=0.62, max_alpha=217):
    """
    Dunkler Verlauf von unten nach oben, unten max_alpha (85 Prozent bei 217).
    Wird über das Foto gelegt, height_frac bestimmt wie hoch der Verlauf
    hinaufreicht.
    """
    grad = Image.new("L", (1, H), 0)
    start = int(H * (1 - height_frac))
    for y in range(H):
        if y < start:
            a = 0
        else:
            t = (y - start) / max(1, (H - 1 - start))
            a = int(max_alpha * (t ** 1.4))
        grad.putpixel((0, y), a)
    grad = grad.resize((W, H))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    overlay.putalpha(grad)
    return overlay


def _draw_arrow(draw, x, y, size, color, thickness=None):
    """
    Pfeil → als Vektorform zeichnen, nicht als Font-Glyph. Quicksand hat kein
    Arrow-Glyph, sondern liefert dafuer ein leeres .notdef-Kaestchen, das im
    Bild wie ein Platzhalter aussieht. x, y ist die obere linke Ecke der
    Bounding Box, size die Zielhoehe. Gibt die benutzte Breite zurueck.
    """
    h = size * 0.5
    w = size * 0.9
    thickness = thickness or max(2, int(round(size * 0.09)))
    cy = y + size * 0.5
    shaft_x2 = x + w * 0.55
    draw.line([(x, cy), (shaft_x2, cy)], fill=color, width=thickness)
    tip = (x + w, cy)
    top = (shaft_x2, cy - h * 0.5)
    bot = (shaft_x2, cy + h * 0.5)
    draw.polygon([tip, top, bot], fill=color)
    return w


def _draw_text_with_arrow(base, draw, x, y, text, f, color, max_w, line_h_factor=1.35, gap=14):
    """
    Text umbrechen und zeichnen, danach einen gezeichneten Pfeil an das Ende
    der letzten Zeile haengen (mit Vorlauf-Leerzeichen). Passt der Pfeil
    nicht mehr auf die letzte Zeile, bekommt er eine eigene Zeile.
    Gibt die y-Position nach dem Block zurueck.
    """
    arrow_size = f.size * 0.62
    arrow_w = arrow_size * 0.9
    reserved = arrow_w + gap

    lines = _wrap(draw, text, f, max_w - reserved)
    # Pruefen, ob die letzte Zeile mit voller Breite (ohne Reserve) plus Pfeil passt.
    if lines:
        last_w, _ = _measure(draw, lines[-1], f)
        if last_w + gap + arrow_w > max_w:
            lines = _wrap(draw, text, f, max_w)

    lh = int(f.size * line_h_factor)
    cur_y = y
    for i, line in enumerate(lines):
        _draw_line(base, draw, (x, cur_y), line, f, color)
        if i == len(lines) - 1:
            lw, _ = _measure(draw, line, f)
            ax = x + lw + gap
            ay = cur_y + (f.getmetrics()[0] - arrow_size) * 0.55
            if ax + arrow_w > x + max_w:
                cur_y += lh
                _draw_arrow(draw, x, cur_y + (f.getmetrics()[0] - arrow_size) * 0.55, arrow_size, color)
            else:
                _draw_arrow(draw, ax, ay, arrow_size, color)
        cur_y += lh
    return cur_y


def _badge(base, draw, x, y, text, dark_bg=True):
    """
    Badge-Pill: dunkelblau halbtransparent auf Foto, Versalien, weiß, weiter
    Buchstabenabstand. Gibt die Höhe der Pille zurück.
    """
    f = font(28, bold=True)
    tracked = "  ".join(list(text.upper()))  # weiter Buchstabenabstand
    tw, th = _measure(draw, tracked, f)
    pad_x, pad_y = 26, 16
    w = int(tw + 2 * pad_x)
    h = int(f.size * 1.1 + 2 * pad_y)

    if dark_bg:
        fill = (15, 29, 51, 214)
    else:
        fill = (255, 255, 255, 40)

    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle([0, 0, w, h], radius=h // 2, fill=fill)
    base.alpha_composite(pill, (int(x), int(y)))

    _draw_line(base, draw, (x + pad_x, y + pad_y - 2), tracked, f, WHITE)
    return h


def _headline(base, draw, x, y, lines, size=84, max_w=None):
    """Zweizeilige Headline, Versalien fett. Zeile 1 weiß, Zeile 2 rot."""
    f = font(size, bold=True)
    colors = [WHITE, RED]
    cur_y = y
    for i, line in enumerate(lines[:2]):
        text = line.upper()
        if max_w:
            fitted = size
            while fitted > 36 and _measure(draw, text, font(fitted, bold=True))[0] > max_w:
                fitted -= 2
            f = font(fitted, bold=True)
        _draw_line(base, draw, (x, cur_y), text, f, colors[i % 2])
        asc, desc = f.getmetrics()
        cur_y += int((asc + desc) * 1.06)
    return cur_y


def _logo(base, draw, x, y, light=True):
    """
    Platzhalter-Logo unten links: K im Kreis, daneben KÖRPER (fett) ueber
    VERWANDLUNG (leicht). Kein echtes Markenasset, siehe Hinweis im Auftrag.
    """
    d = 46
    ring_col = WHITE if light else NAVY
    fill_col = (255, 255, 255, 235) if light else (15, 29, 51, 235)
    text_col = NAVY if light else WHITE

    circ = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(circ)
    cdraw.ellipse([0, 0, d, d], fill=fill_col)
    base.alpha_composite(circ, (int(x), int(y)))

    fk = font(24, bold=True)
    kw, _ = _measure(draw, "K", fk)
    _draw_line(base, draw, (x + (d - kw) / 2, y + d * 0.20), "K", fk, text_col)

    tx = x + d + 14
    f_bold = font(20, bold=True)
    f_light = font(20, bold=False)
    _draw_line(base, draw, (tx, y + 1), "KÖRPER", f_bold, ring_col)
    _draw_line(base, draw, (tx, y + 22), "VERWANDLUNG", f_light, ring_col)


def _bullets(base, draw, x, y, bullets, max_w, lead_size=32, cont_size=32, gap=26, icon=44):
    """
    Bulletpoints im Hausstil: rotes abgerundetes Quadrat mit weißem Pfeil,
    Text startet halbfett weiß (Lead-Phrase) und läuft grau weiter.
    Höchstens zwei Zeilen pro Bullet. Gibt die Endposition y zurück.
    """
    text_x = x + icon + 18
    text_w = max_w - icon - 18

    f_lead = font(lead_size, bold=True)
    f_cont = font(cont_size, bold=False)

    cur_y = y
    for lead, cont in bullets:
        sq = Image.new("RGBA", (icon, icon), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(sq)
        sdraw.rounded_rectangle([0, 0, icon, icon], radius=10, fill=RED)
        a_size = icon * 0.46
        aw = a_size * 0.9
        _draw_arrow(sdraw, (icon - aw) / 2, (icon - a_size) / 2, a_size, WHITE)
        base.alpha_composite(sq, (int(x), int(cur_y)))

        full = f"{lead}: {cont}"
        lh = int(f_lead.size * 1.28)
        lines = _wrap(draw, full, f_lead, text_w)  # nur zum Umbrechen, Breite gleich

        ly = cur_y + 2
        lead_done = False
        remaining_lead = lead
        for line in lines[:2]:
            lx = text_x
            if not lead_done and line.startswith(remaining_lead[: min(len(remaining_lead), len(line))]):
                # Lead-Phrase (mit folgendem Doppelpunkt) in dieser Zeile halbfett weiß,
                # Rest der Zeile grau.
                split_at = len(lead) + 1 if line.startswith(lead + ":") else len(line)
                lead_part = line[:split_at]
                rest_part = line[split_at:]
                _draw_line(base, draw, (lx, ly), lead_part, f_lead, WHITE)
                lw, _ = _measure(draw, lead_part, f_lead)
                if rest_part:
                    _draw_line(base, draw, (lx + lw, ly), rest_part, f_cont, GREY)
                lead_done = True
            else:
                _draw_line(base, draw, (lx, ly), line, f_cont, GREY)
            ly += lh

        block_h = max(icon, ly - cur_y)
        cur_y += block_h + gap

    return cur_y - gap  # letzte Luecke nicht mitzaehlen, der Aufrufer setzt seinen eigenen Abstand


def _watermark_number(base, number):
    """Große Ziffer der Slide als Wasserzeichen rechts, sehr dunkles Blau."""
    f = font(560, bold=True)
    draw = ImageDraw.Draw(base)
    tw, th = _measure(draw, number, f)
    x = W - tw + 60
    y = H - th - 40
    _draw_line(base, draw, (x, y), number, f, NAVY_WATERMARK)


def _rings(base):
    """Dezente dünne Kreislinien als Struktur, sehr geringer Kontrast."""
    draw = ImageDraw.Draw(base)
    specs = [
        (-180, -160, 620),
        (W - 120, H - 260, 480),
        (W * 0.55, -260, 520),
    ]
    for cx, cy, r in specs:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY_RING, width=2)


# --------------------------------------------------------------------------
# Öffentliche Render-Funktionen
# --------------------------------------------------------------------------

def render_photo_slide(
    photo,
    out,
    badge,
    headline,
    sub=None,
    bullets=None,
    cta=None,
    face_anchor=0.32,
    gradient_height=0.62,
    gradient_alpha=217,
    zoom=1.0,
    crop_x=0,
    content_top=None,
    headline_max_w=None,
):
    """
    Cover- oder Schluss-Slide auf Fotobasis, 1080 x 1350.

    photo         Pfad zum Foto
    out           Zielpfad
    badge         Kurzes Schlagwort für die Badge-Pill
    headline      Liste mit 2 Zeilen, Zeile 1 weiß, Zeile 2 rot
    sub           Optionale Sub-Zeile mit Pfeil (nur Cover, ohne "→")
    bullets       Optionale Liste von (lead, cont)-Tupeln für die Schluss-Slide
    cta           Optionaler Handlungssatz unter den Bullets, ohne "→"
    face_anchor   0 bis 1, wo im Originalfoto das Gesicht sitzt. Bei Fotos, die
                  fast bildfuellend sind, bleibt kaum Spielraum: focus=0.0
                  schneidet so wenig wie moeglich vom Kinn ab und schafft
                  darunter maximal Platz fuer den Textblock.
    content_top   0 bis 1, wo der Textblock startet. Ohne Angabe 0.64 fuer
                  reine Cover-Slides, 0.665 wenn Bullets vorliegen (die
                  Schluss-Slide braucht mehr Platz und muss unterhalb des
                  Kinns beginnen, sonst liegt Text im Gesicht)
    headline_max_w  Eigene Breitenbegrenzung fuer die Headline, wenn eine
                  Geste im Foto weiter in den Textbereich hineinragt und die
                  volle Breite mit ihr kollidieren wuerde. Die Headline
                  schrumpft automatisch, bis sie darunter passt.
    """
    base = _cover(photo, focus=face_anchor, zoom=zoom, crop_x=crop_x).convert("RGBA")
    base.alpha_composite(_gradient_overlay(height_frac=gradient_height, max_alpha=gradient_alpha))
    draw = ImageDraw.Draw(base)

    if content_top is not None:
        y = int(H * content_top)
    elif bullets:
        y = int(H * 0.65)
    else:
        y = int(H * 0.64)

    bh = _badge(base, draw, MARGIN, y, badge, dark_bg=True)
    y += bh + (10 if bullets else 26)

    hsize = 50 if bullets else 84
    hmw = headline_max_w if headline_max_w else W - 2 * MARGIN
    y = _headline(base, draw, MARGIN, y, headline, size=hsize, max_w=hmw)
    y += 2 if bullets else 6

    if sub:
        f_sub = font(33)
        y = _draw_text_with_arrow(base, draw, MARGIN, y, sub, f_sub, WHITE, W - 2 * MARGIN)
        y += 10

    if bullets:
        y += 10
        y = _bullets(base, draw, MARGIN, y, bullets, W - 2 * MARGIN,
                     lead_size=24, cont_size=24, gap=8, icon=32)

    if cta:
        y += 4 if bullets else 6
        f_cta = font(24, bold=True) if bullets else font(30, bold=True)
        y = _draw_text_with_arrow(base, draw, MARGIN, y, cta, f_cta, RED, W - 2 * MARGIN)

    bottom_limit = H - 40
    if y > bottom_limit:
        print(
            f"  Warnung: Inhalt in {os.path.basename(out)} laeuft unten aus dem "
            f"Bild ({int(y)} von {H} px).",
            file=sys.stderr,
        )

    _logo(base, draw, MARGIN, H - 40 - 46, light=True)

    base.convert("RGB").save(out, "PNG")
    return out


def render_content_slide(
    out,
    number,
    badge,
    headline,
    bullets,
    outro=None,
):
    """
    Inhalts-Slide, Hintergrund #0F1D33, 1080 x 1350.

    out        Zielpfad
    number     Ziffer der Slide als String, z. B. "02", fuers Wasserzeichen
    badge      Kurzes Schlagwort fuer die Badge-Pill oben links
    headline   Liste mit 2 Zeilen, Zeile 1 weiss, Zeile 2 rot
    bullets    Liste von genau 3 (lead, cont)-Tupeln
    outro      Optionales (zeile1, zeile2)-Tupel als Abbinder, zeile1 grau,
               zeile2 rot und fett
    """
    base = Image.new("RGBA", (W, H), NAVY + (255,))
    _rings(base)
    _watermark_number(base, number)
    draw = ImageDraw.Draw(base)

    y = 92
    bh = _badge(base, draw, MARGIN, y, badge, dark_bg=False)
    y += bh + 18

    draw.rectangle([MARGIN, y, MARGIN + 70, y + 6], fill=RED)
    y += 34

    y = _headline(base, draw, MARGIN, y, headline, size=78, max_w=W - 2 * MARGIN)
    y += 44

    y = _bullets(base, draw, MARGIN, y, bullets, W - 2 * MARGIN,
                 lead_size=33, cont_size=33, gap=32)

    y += 18 + 32  # Bulletabstand nachholen, _bullets zaehlt die letzte Luecke nicht mit
    draw.line([MARGIN, y, W - MARGIN, y], fill=NAVY_RING, width=2)
    y += 34

    if outro:
        f1 = font(30)
        f2 = font(34, bold=True)
        l1, l2 = outro
        _draw_line(base, draw, (MARGIN, y), l1, f1, GREY)
        y += int(f1.size * 1.35)
        _draw_line(base, draw, (MARGIN, y), l2, f2, RED)
        y += int(f2.size * 1.3)

    bottom_limit = H - 40
    if y > bottom_limit:
        print(
            f"  Warnung: Inhalt in {os.path.basename(out)} laeuft unten aus dem "
            f"Bild ({int(y)} von {H} px).",
            file=sys.stderr,
        )

    _logo(base, draw, MARGIN, H - 40 - 46, light=True)

    base.convert("RGB").save(out, "PNG")
    return out
