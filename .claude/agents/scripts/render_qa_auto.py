import sys, os
sys.path.insert(0, "/home/user/Claude-Code-/.claude/agents/scripts")
from story_slide import render_slide

S = "/tmp/claude-0/-home-user-Claude-Code-/7fc6a235-3a1c-5ad1-bf15-b37cbdff4250/scratchpad"
OUT = sys.argv[1] if len(sys.argv) > 1 else S + "/auto_slides"
os.makedirs(OUT, exist_ok=True)

# Peter-Befund: Format B erlaubt normalerweise 2 bis 3 Slides, nicht 4 (die
# 4-Slide-Ausnahme gilt sonst nur fuer Format C mit eingebettetem Reel). Der
# Nutzer wollte hier ausdruecklich alle vier Antworten behalten, Peter hat das
# als bewusste Nutzervorgabe akzeptiert und freigegeben (dieselbe Logik wie bei
# Tanjas Kundengeschichte), inklusive Pruefung der Ja-Haeufung: 3 von 4 Antworten
# beginnen mit Ja, das deckt sich mit dem Muster in den Bestandsbeispielen.
SLIDES = [
    {"foto": 1, "sticker": "muss ich mein ganzes essen umstellen?",
     "boxes": ["Nein, keine radikale umstellung",
               "wir verändern schritt für schritt, was zu deinem alltag passt."]},
    {"foto": 2, "sticker": "ist bewegung wichtig?",
     "boxes": ["Ja", "aber du brauchst kein hartes training, jede bewegung zählt."]},
    {"foto": 3, "sticker": "geht das auch, wenn ich unsportlich bin?",
     "boxes": ["Ja, absolut", "der einstieg ist für jeden möglich, ganz ohne vorerfahrung."]},
    {"foto": 4, "sticker": "darf ich dann süßigkeiten essen?",
     "boxes": ["Ja, klar", "weil es auf die menge ankommt, nicht auf strenge verbote."]},
]

for i, s in enumerate(SLIDES, start=1):
    render_slide(
        photo=f"{S}/auto_norm/foto_{s['foto']}.jpg",
        out=f"{OUT}/slide_{i:02d}.png",
        sticker=s["sticker"], boxes=s["boxes"],
        top=0.05, box_size=40, align="right", max_width=0.46,
    )
    print(f"{OUT}/slide_{i:02d}.png")
