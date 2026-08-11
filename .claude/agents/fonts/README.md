# Schriftdateien

Hier gehören die Schriften hin, die die Render-Skripte benutzen.

## Decor

Projektvorgabe für alle Story-Texte. **Die Datei fehlt aktuell.**

Lege sie hier als `Decor.ttf` oder `Decor.otf` ab, optional zusätzlich
`Decor-Bold.ttf` für die fetten Stellen. Die Skripte finden sie dann automatisch,
es ist keine weitere Änderung nötig.

Solange Decor fehlt, rendert `scripts/story_slide.py` mit **URW Gothic**, der
nächstliegenden geometrischen Rundschrift auf dem System, und gibt eine Warnung aus.
Diese Warnung wird an den Nutzer weitergegeben.
