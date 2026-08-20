import sys, os
sys.path.insert(0, "/home/user/Claude-Code-/.claude/agents/scripts")
from story_slide import render_slide

S = "/tmp/claude-0/-home-user-Claude-Code-/7fc6a235-3a1c-5ad1-bf15-b37cbdff4250/scratchpad"
OUT = sys.argv[1] if len(sys.argv) > 1 else S + "/auto_slides"
os.makedirs(OUT, exist_ok=True)

# Peter-Befund: Format B erlaubt 2 bis 3 Slides, nicht 4 (die 4-Slide-Ausnahme
# gilt nur fuer Format C mit eingebettetem Reel). "ist bewegung wichtig?" ist
# deshalb zurueckgestellt fuer eine kuenftige Runde, siehe SLIDES_ZURUECKGESTELLT.
SLIDES = [
    {"foto": 1, "sticker": "muss ich mein ganzes essen umstellen?",
     "boxes": ["Nein, keine radikale umstellung",
               "wir verändern schritt für schritt, was zu deinem alltag passt."]},
    {"foto": 3, "sticker": "geht das auch, wenn ich unsportlich bin?",
     "boxes": ["Ja, absolut", "der einstieg ist für jeden möglich, ganz ohne vorerfahrung."]},
    {"foto": 4, "sticker": "darf ich dann süßigkeiten essen?",
     "boxes": ["Ja, klar 😉", "weil es auf die menge ankommt, nicht auf strenge verbote."]},
]

SLIDES_ZURUECKGESTELLT = [
    {"foto": 2, "sticker": "ist bewegung wichtig?",
     "boxes": ["Ja", "aber du brauchst kein hartes training, jede bewegung zählt."]},
]

for i, s in enumerate(SLIDES, start=1):
    render_slide(
        photo=f"{S}/auto_norm/foto_{s['foto']}.jpg",
        out=f"{OUT}/slide_{i:02d}.png",
        sticker=s["sticker"], boxes=s["boxes"],
        top=0.05, box_size=40, align="right", max_width=0.46,
    )
    print(f"{OUT}/slide_{i:02d}.png")
