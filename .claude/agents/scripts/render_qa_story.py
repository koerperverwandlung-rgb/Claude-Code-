#!/usr/bin/env python3
"""
Frage-Antwort-Story rendern, fertige Slides aus einem Ordner mit Fotos.

Benutzung:
    python3 render_qa_story.py <foto-ordner> [ziel-ordner]

Erwartet im Foto-Ordner die Dateien foto_1.jpg bis foto_4.jpg. JPG, JPEG, PNG und
HEIC-Ableger werden erkannt, die Endung ist egal, solange die Nummer stimmt.

Die Texte stehen unten in SLIDES und stammen von Sabine. Zum Ändern einfach dort
anpassen und neu laufen lassen.
"""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_slide import render_slide  # noqa: E402

# Sabines Texte. Reihenfolge ist die Reihenfolge in der Story.
# foto      welche Fotonummer als Hintergrund
# top       Startpunkt des Textblocks als Anteil der Bildhöhe
# size      Schriftgröße der Antwortkästen
SLIDES = [
    # Peter-Befund: Foto 1 (ohne Geste) traegt dieses Format nicht. Das Gesicht sitzt
    # mittig und die Kappe beginnt bei y 620. Zwischen Instagrams Kopfleiste und der
    # Kappe bleiben rund 470 px, der Sticker allein braucht schon 290. Deshalb drei
    # Slides mit den Gesten-Fotos, dort ist das Gesicht links und rechts bleibt Platz.
    {
        "foto": 3,
        "sticker": "in den wechseljahren klappt das doch eh nicht, oder...",
        "boxes": [
            "Doch, aber anders",
            "Dein Stoffwechsel braucht jetzt andere Reize als mit 30.",
        ],
        "top": 0.086, "size": 38, "align": "right", "max_width": 0.46,
        "crop_x": 0,
    },
    {
        "foto": 2,
        "sticker": "ich hab schon so viel probiert... warum soll das klappen?",
        "boxes": [
            "Nicht du hast versagt",
            "Die Diäten waren der falsche Weg, nicht dein Körper.",
        ],
        # Ausschnitt maximal nach links, sonst schneidet der mittige Beschnitt
        # das Gesicht an
        "top": 0.086, "size": 38, "align": "right", "max_width": 0.46,
        "crop_x": -180,
    },
    {
        "foto": 4,
        "sticker": "ich arbeite voll und hab familie... schaff ich das überhaupt?",
        "boxes": [
            "Ja, das schaffst du",
            "Wir bauen alles in deinen Alltag ein.",
        ],
        "top": 0.086, "size": 38, "align": "right", "max_width": 0.46,
        "crop_x": 0,
    },
]


def finde_foto(ordner, nummer):
    treffer = sorted(glob.glob(os.path.join(ordner, f"foto_{nummer}.*")))
    if not treffer:
        raise SystemExit(
            f"Kein Foto foto_{nummer}.* in {ordner} gefunden. "
            f"Vorhanden: {sorted(os.listdir(ordner))}"
        )
    return treffer[0]


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    quelle = sys.argv[1]
    ziel = sys.argv[2] if len(sys.argv) > 2 else os.path.join(quelle, "slides")
    os.makedirs(ziel, exist_ok=True)

    erzeugt = []
    for i, s in enumerate(SLIDES, start=1):
        out = os.path.join(ziel, f"slide_{i:02d}.png")
        render_slide(
            photo=finde_foto(quelle, s["foto"]),
            out=out,
            sticker=s["sticker"],
            boxes=s["boxes"],
            top=s["top"],
            box_size=s["size"],
            align=s.get("align", "center"),
            max_width=s.get("max_width", 0.86),
            sticker_width=s.get("sticker_width", 0.64),
            crop_x=s.get("crop_x", 0),
        )
        erzeugt.append(out)
        print(out)
    print(f"\n{len(erzeugt)} Slides erzeugt in {ziel}")


if __name__ == "__main__":
    main()
