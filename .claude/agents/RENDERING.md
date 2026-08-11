# Fertige Bilddateien statt Textentwürfe

Gilt für **Sabine**, **Sarah** und **Thumbnail Tom**. Peter prüft gegen diese Datei mit.

## Die Grundregel

Wenn der Nutzer sagt **"erstell das"**, **"erstell die Slides"**, **"erstell das Bild"**
oder etwas Gleichbedeutendes, will er **fertige Bilddateien**, keine Beschreibung.

Falsch:
```
Kasten 1: Nie zu spät
Kasten 2: Dein Körper reagiert in jedem Alter auf gute Gewohnheiten.
Platzierung: oben rechts
```

Richtig: eine gerenderte PNG-Datei, in der genau das schon drin steht, ausgeliefert per
`SendUserFile`, sodass der Nutzer sie direkt hochladen kann.

Ein reiner Textentwurf ist nur dann die richtige Antwort, wenn der Nutzer ausdrücklich
nach Texten, Entwürfen oder Vorschlägen fragt, oder wenn du in der Abnahmeschleife
stehst und die Texte vor dem Rendern freigeben lässt. Sobald "erstell" fällt, wird
gerendert.

## Ablauf

1. **Fotos prüfen.** Du brauchst die Bilddateien auf der Platte. Hochgeladene Bilder,
   die du nur im Chat siehst, liegen nicht zwangsläufig als Datei vor. Prüfe den
   Upload-Ordner. Wenn die Dateien fehlen, sagst du das sofort und bittest um die Fotos,
   statt einen Textentwurf als Ersatz zu liefern.
2. **Texte festlegen**, nach den Regeln deines Profils.
3. **Rendern** mit dem Skript unten.
4. **Ergebnis ansehen.** Öffne jede erzeugte Datei und schau sie dir an. Prüfe, ob Text
   über dem Gesicht liegt, ob etwas aus dem Bild läuft, ob die Kästen sitzen. Wenn nicht,
   korrigierst du die Werte und renderst neu.
5. **Ausliefern** per `SendUserFile`, alle Dateien zusammen, mit einer kurzen Bildunterschrift.

## Das Skript für Story-Slides

`.claude/agents/scripts/story_slide.py` baut 1080 × 1920 Slides mit weißen Kästen,
schwarzer Schrift, zentriert, plus optionalem Fragensticker.

```python
import sys
sys.path.insert(0, ".claude/agents/scripts")
from story_slide import render_slide

render_slide(
    photo="pfad/zum/foto.jpg",
    out="slide_01.png",
    sticker="ich bin 54... ist es dafür nicht zu spät?",  # None wenn kein Sticker
    boxes=[
        "Nie zu spät",
        "Dein Körper reagiert in jedem Alter auf gute Gewohnheiten. 💫",
    ],
    top=0.10,        # Startpunkt des Blocks, Anteil der Bildhöhe
    align="center",  # center, left, right
    box_size=58,     # Schriftgröße der Antwortkästen
)
```

Nützliche Stellschrauben:

| Parameter | Wofür |
|---|---|
| `top` | Block höher oder tiefer setzen, damit das Gesicht frei bleibt |
| `align` | Kästen links oder rechts setzen, wenn im Bild eine Geste frei bleiben soll |
| `box_size` | Schrift kleiner, wenn der Text sonst zu viel Platz frisst |
| `first_box_size` | Kasten 1 größer setzen, wenn er die Kernaussage trägt |
| `gap` | Abstand zwischen den Kästen |
| `max_width` | Breite des Satzspiegels, Standard 86 Prozent |

Das Skript warnt auf stderr, wenn der Textblock unten aus dem Bild läuft. Diese Warnung
ignorierst du nie, sondern kürzt den Text oder setzt `top` kleiner.

Das Foto wird immer mittig auf 1080 × 1920 beschnitten, ohne Verzerrung. Wenn der
wichtige Bildteil dabei wegfällt, schneidest du das Foto vorher selbst passend zu.

## Schriftart

Projektvorgabe für alle Story-Texte ist **Decor**. Die Schriftdatei liegt aktuell nicht
im Projekt. Solange sie fehlt, setzt das Skript automatisch **URW Gothic**, die
nächstliegende geometrische Rundschrift, und gibt eine Warnung aus.

Diese Warnung gibst du beim Ausliefern an den Nutzer weiter, einmal pro Auftrag, kurz.
Sobald `Decor.ttf` oder `Decor.otf` in `.claude/agents/fonts/` liegt, wird sie ohne
weitere Änderung benutzt.

## Emojis

Farb-Emojis werden aus NotoColorEmoji gerendert und als Bild in die Zeile gesetzt, auch
mit Hautton. Du schreibst sie einfach in den Text, um den Rest kümmert sich das Skript.

## Karussells und Thumbnails

Für Karussell-Beiträge, 1080 × 1350, und für Thumbnails, 1280 × 720, gibt es noch kein
fertiges Skript. Du schreibst dir für den jeweiligen Auftrag ein eigenes mit Pillow,
hältst dich dabei an die Gestaltungsvorgaben aus deinem Profil und lieferst ebenfalls
fertige Dateien. Wenn dabei etwas entsteht, das mehrfach nützlich ist, legst du es unter
`.claude/agents/scripts/` ab.

## Dateinamen

Durchnummeriert und sprechend, damit die Reihenfolge klar ist:
```
slide_01.png  slide_02.png  slide_03.png
thumbnail_a.png  thumbnail_b.png  thumbnail_c.png
```
