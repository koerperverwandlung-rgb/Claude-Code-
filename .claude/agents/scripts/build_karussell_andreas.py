import sys
sys.path.insert(0, "/home/user/Claude-Code-/.claude/agents/scripts")
from render_karussell import render_photo_slide, render_content_slide

BASE = "/tmp/claude-0/-home-user-Claude-Code-/7fc6a235-3a1c-5ad1-bf15-b37cbdff4250/scratchpad"
OUT = f"{BASE}/karussell_andreas"

PHOTO_COVER = f"{BASE}/fotos_neu/foto_1.jpg"
PHOTO_CLOSE = f"{BASE}/fotos_neu/foto_2.jpg"

# Slide 1, Cover
render_photo_slide(
    photo=PHOTO_COVER,
    out=f"{OUT}/slide_01.png",
    badge="ERSTER SCHRITT",
    headline=["DIE KÖRPERANALYSE", "VERÄNDERT ALLES"],
    sub="Warum die Waage nie die ganze Wahrheit zeigt",
    face_anchor=0.30,
    # Peter-Befund: die volle Headline-Breite kreuzt den erhobenen Zeigefinger.
    # Der Ausschnitt hat kaum Spielraum (Foto laesst sich per crop_x praktisch
    # nicht verschieben), deshalb schrumpft die Headline stattdessen unter die
    # Fingerposition, die bei etwa x=700 beginnt.
    headline_max_w=600,
)

# Slide 2, Inhalt
render_content_slide(
    out=f"{OUT}/slide_02.png",
    number="02",
    badge="KÖRPERWERTE",
    headline=["WAS DEINE", "WAAGE VERSCHWEIGT"],
    bullets=[
        ("Muskelmasse", "zeigt, wie viel deines Gewichts wirklich Kraft ist."),
        ("Wasserhaushalt", "erklärt, warum die Zahl täglich schwankt."),
        ("Fettverteilung", "zeigt Veränderung, auch wenn die Waage stillsteht."),
    ],
    outro=(
        "Eine Zahl allein erklärt nie die ganze Geschichte.",
        "Deine Körperanalyse schon.",
    ),
)

# Slide 3, Inhalt
render_content_slide(
    out=f"{OUT}/slide_03.png",
    number="03",
    badge="DER ABLAUF",
    headline=["DEIN TERMIN BEI", "KÖRPERVERWANDLUNG"],
    bullets=[
        ("Das Gespräch", "wir hören uns an, wo du gerade stehst."),
        ("Die Messung", "wenige Minuten, ganz ohne unangenehme Fragen."),
        ("Der Befund", "wir lesen die Werte gemeinsam mit dir."),
    ],
    outro=(
        "Kein Test, den du allein auswerten musst.",
        "Wir schauen gemeinsam drauf.",
    ),
)

# Slide 4, Inhalt
render_content_slide(
    out=f"{OUT}/slide_04.png",
    number="04",
    badge="DEIN VORTEIL",
    headline=["WARUM DAS DEN", "UNTERSCHIED MACHT"],
    bullets=[
        ("Ein Ausgangspunkt", "du weißt endlich, woran wir arbeiten."),
        ("Ein Plan für dich", "deine Werte bestimmen dein Tempo."),
        ("Ein fester Termin", "so siehst du, was sich verändert hat."),
    ],
    outro=(
        "Fortschritt, den du nicht erraten musst.",
        "Sondern schwarz auf weiß siehst.",
    ),
)

# Slide 5, Schluss
render_photo_slide(
    photo=PHOTO_CLOSE,
    out=f"{OUT}/slide_05.png",
    badge="WORAUF ES ANKOMMT",
    headline=["DEIN ERSTER SCHRITT", "BEGINNT HIER"],
    bullets=[
        ("Ohne Verpflichtung", "ein Gespräch, das dir zeigt, wo du stehst."),
        ("Ohne Rätselraten", "klare Werte statt vagem Gefühl."),
        ("Mit Begleitung", "du weißt, was als nächstes kommt."),
    ],
    cta="Schreib mir und sichere dir deine Körperanalyse",
    face_anchor=0.0,
    gradient_height=0.78,
    gradient_alpha=235,
)

print("fertig")
