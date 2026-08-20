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

Projektvorgabe für alle Story-Texte ist **Decor**. Das ist eine der Schriften aus dem
Instagram-eigenen Story-Texteditor, fest in die App einkompiliert. Instagram gibt diese
Schriftdateien nicht heraus, Decor ist deshalb grundsätzlich nicht als Datei zu
beschaffen, außer das Team hat sie selbst irgendwo lizenziert. Solange keine Datei im
Projekt liegt, setzt das Skript automatisch **Quicksand Medium**.

Quicksand wurde am 2026-08-18 direkt gegen ein Original-Referenzbild aus dem Bestand
verglichen, Buchstabe für Buchstabe, und trifft die Formen fast deckungsgleich, näher
als jede andere auf dem System verfügbare Schrift. Beim Feinabgleich stellte sich
heraus, dass der Schnitt **Medium** und nicht Regular der richtige ist: Regular war im
direkten Pixelvergleich zu dünn, Medium trifft Strichstärke und Zeilenbreite der
Originalzeile fast exakt (bei gleicher Textbreite lagen beide innerhalb weniger Pixel).
Das ist bis auf Weiteres der beste verfügbare Ersatz für Decor, kein Notbehelf mehr.

Diese Warnung gibst du beim Ausliefern an den Nutzer weiter, einmal pro Auftrag, kurz.
Sobald `Decor.ttf` oder `Decor.otf` in `.claude/agents/fonts/` liegt, wird sie ohne
weitere Änderung benutzt und hat automatisch Vorrang vor Quicksand.

## Format C, Kundengeschichte rendern

Für die mehrteilige Kundengeschichte, siehe Format C in `sabine.md`, gibt es die
Funktion `render_stacked_boxes` im selben Skript. Sie zeichnet mehrere gestapelte
weiße Kästen ohne Fragensticker, Text im Kasten immer linksbündig, so wie im
Referenzbeispiel aus dem Bestand.

```python
from story_slide import render_stacked_boxes

render_stacked_boxes(
    photo="pfad/zum/foto.jpg",
    out="slide_01.png",
    boxes=[
        ("Das war Tanja vor ihrer Körperverwandlung:", 40),  # Tupel = eigene Größe
        "👉🏼 Der Blick in den Spiegel, den sie am liebsten vermied",
        "👉🏼 Kleidung, die sich jeden Tag enger anfühlte",
        "Dann kam ihre erste Körperanalyse...",
    ],
    top=0.30,          # Startpunkt des ersten Kastens
    align="left",      # left, right oder center, Position der ganzen Kastenspalte
    default_size=34,   # Schriftgröße ohne eigene Angabe
    gap=14,
)
```

Ein Eintrag in `boxes` ist entweder ein String in Standardgröße, oder ein
`(text, size)`-Tupel für einen größer gesetzten Kasten, etwa den Einstiegssatz oder
die Kernaussage "Tanja hat es geschafft!". Ein `\n` im Text erzwingt einen Zeilenumbruch,
nützlich für die Zahl, wenn sie auf eigenen Zeilen stehen soll, zum Beispiel
`"-15,4 KG\n-16,5 CM BAUCHUMFANG\nin 4 Monaten"`.

Vor dem Rendern ein Raster über das Foto legen und nachsehen, wo Gesicht und wichtige
Gesten sitzen, siehe `_cover` und die Beispiele in den bisherigen Aufträgen. Kästen
dürfen über Armen, Händen und Beinen liegen, nie über einem Gesicht.

## Emojis

Farb-Emojis werden aus NotoColorEmoji gerendert und als Bild in die Zeile gesetzt, auch
mit Hautton. Du schreibst sie einfach in den Text, um den Rest kümmert sich das Skript.

Der Nutzer hat am 2026-08-20 bemängelt, dass die Emojis nicht wie klassische
iPhone-Emojis aussehen und nicht hochwertig wirken. Geprüft wurde das Gleiche wie bei
Decor: Apples eigene Emoji-Grafiken sind proprietär und stehen auf keinem Server
legal zur Verfügung, eine echte iPhone-Optik lässt sich also nicht direkt beschaffen.
Als Alternative wurde `fonts-emojione` (Emoji One, Stand 2016) installiert und an
denselben Emojis direkt gegen NotoColorEmoji verglichen: Emoji One ist flacher, hat
kaum Schattierung und wirkt kantiger, an mehreren Stellen (Schokolade, Sterne)
außerdem farblich unstimmig, insgesamt sichtbar altbacken und nicht hochwertiger.
Symbola wurde verworfen, ohne es zu rendern, weil es kein Farb-Emoji-Font ist, sondern
ein einfarbiger Symbolzeichensatz. Ein Blick in zwei bereits ausgelieferte, echte
Slides (`😉` und `💪🏼`) in starker Vergrößerung zeigte zudem keinen technischen
Fehler, sauberer Zuschnitt, korrekter Hautton, kein Pixelmatsch. Die installierte
NotoColorEmoji-Version 2.047 ist Googles aktuelles Redesign mit weichen 3D-Verläufen
und Glanzlichtern, das ist stilistisch bereits deutlich näher an Apple als jede alte
Emoji-Generation und bleibt bis auf Weiteres der beste legal verfügbare Ersatz. Diese
Entscheidung ist damit abgeschlossen, nicht bei jedem Auftrag neu zu prüfen, außer es
taucht ein konkreter Renderfehler auf.

## Karussells

`.claude/agents/scripts/render_karussell.py` baut Karussell-Beiträge, 1080 × 1350,
nach der in `sabine.md` dokumentierten Hausvorlage. Zwei Funktionen:

```python
from render_karussell import render_photo_slide, render_content_slide

# Cover- oder Schluss-Slide, Foto mit Verlauf, Badge, Headline, optional Bullets
render_photo_slide(
    photo="andreas.jpg",
    out="slide_01.png",
    badge="ERSTER SCHRITT",
    headline=["DIE KÖRPERANALYSE", "VERÄNDERT ALLES"],  # Zeile 1 weiß, Zeile 2 rot
    sub="Warum die Waage nie die ganze Wahrheit zeigt",   # nur Cover, Pfeil automatisch
    face_anchor=0.30,   # 0 = Gesicht ganz oben im Ausschnitt, 1 = ganz unten
)

# Inhalts-Slide, Dunkelblau, Badge, Headline, genau 3 Bulletpoints, Abbinder
render_content_slide(
    out="slide_02.png",
    number="02",
    badge="KÖRPERWERTE",
    headline=["WAS DEINE", "WAAGE VERSCHWEIGT"],
    bullets=[("Muskelmasse", "sagt mehr über deinen Fortschritt als das Gewicht."), ...],
    abbinder=["Eine Zahl reicht nicht.", "Deine Werte schon."],
)
```

Wenn eine Geste im Foto in den Textbereich hineinragt, wie ein erhobener Finger oder
eine ausgestreckte Hand, prüfst du das per Raster wie bei den Stories und begrenzt bei
Bedarf `headline_max_w` in `render_photo_slide`, damit die Headline automatisch
schrumpft statt die Geste zu überdecken. `crop_x` und `zoom` verschieben den
Bildausschnitt, haben bei bildfüllenden Selfie-Fotos aber oft kaum Spielraum, das
zuerst mit einem Raster prüfen statt blind zu verschieben.

Das Logo unten links ist ein Platzhalter, ein K im Kreis, kein echtes Markenasset. Das
sagst du dem Nutzer bei jeder Auslieferung kurz dazu, bis ein echtes Logo-Bild im
Projekt liegt.

## Thumbnails

Für Thumbnails, 1280 × 720, gibt es noch kein fertiges Skript. Du schreibst dir für den
jeweiligen Auftrag eines mit Pillow, hältst dich an die Gestaltungsvorgaben aus deinem
Profil und lieferst fertige Dateien. Wenn dabei etwas entsteht, das mehrfach nützlich
ist, legst du es unter `.claude/agents/scripts/` ab.

## Dateinamen

Durchnummeriert und sprechend, damit die Reihenfolge klar ist:
```
slide_01.png  slide_02.png  slide_03.png
thumbnail_a.png  thumbnail_b.png  thumbnail_c.png
```
