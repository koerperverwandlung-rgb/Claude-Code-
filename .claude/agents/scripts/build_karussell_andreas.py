import sys
sys.path.insert(0, "/home/user/Claude-Code-/.claude/agents/scripts")
from render_karussell import render_photo_slide, render_content_slide

BASE = "/tmp/claude-0/-home-user-Claude-Code-/7fc6a235-3a1c-5ad1-bf15-b37cbdff4250/scratchpad"
OUT = f"{BASE}/karussell_andreas"

# Nutzer wollte statt der Selfies zwei echte Veranstaltungsfotos: Cover mit den
# beiden Teilnehmerinnen (Beate und Carolin), Schluss mit Andreas verschwommen
# im Hintergrund. Beide Querformat/Hochformat-Fotos aus einer Interview-Session,
# ganz anders zugeschnitten als die bisherigen Selfies.
PHOTO_COVER = f"{BASE}/karussell_fotos_neu/a/Andreas_Beate Siegert_Carolin Steffens_Interview_quer .jpg"
PHOTO_CLOSE = f"{BASE}/karussell_fotos_neu/b/Andreas_Interview_Blass.jpg"

# Slide 1, Cover
render_photo_slide(
    photo=PHOTO_COVER,
    out=f"{OUT}/slide_01.png",
    badge="ERSTER SCHRITT",
    headline=["DIE KÖRPERANALYSE", "VERÄNDERT ALLES"],
    sub="Warum die Waage nie die ganze Wahrheit zeigt",
    face_anchor=0.35,
    # Querformat-Foto, 6048x4032. Per Raster geprueft: crop_x=180 zeigt beide
    # Teilnehmerinnen (Beate links, Carolin rechts) vollstaendig und mittig,
    # Andreas bleibt wie gewuenscht nur als Hand/Knie am unteren linken Rand.
    crop_x=180,
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
    cta="Schreib mir und sichere dir dein Erstgespräch",
    # Hochformat-Foto, 4160x6240, Andreas verschwommen im Hintergrund neben der
    # Kamera. Gesicht sitzt bei focus=0 bereits weit oben (um y300), Textblock
    # startet erst deutlich darunter, keine Kollision. Gradient wie zuvor
    # geprueft, Kontrast hier zusaetzlich durch die dunkle Kamera im Vordergrund.
    face_anchor=0.0,
    gradient_height=0.78,
    gradient_alpha=235,
)

print("fertig")
