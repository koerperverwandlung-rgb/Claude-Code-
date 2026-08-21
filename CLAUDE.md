# Projektnotizen für Claude

## Nutzer-Präferenzen

- **Klickbare Links**: Wenn der Nutzer eine Web-Seite, App oder ein Tool erstellt bekommt,
  IMMER einen direkten klickbaren Hyperlink in der Antwort ausgeben, mit dem die
  Anwendung sofort im Browser geöffnet werden kann (z. B. via raw.githack.com,
  GitHub Pages, Vercel-Preview o. ä.). Nicht nur erklären, wie man sie deployt,
  sondern einen funktionierenden Link liefern.
- **URL bei jedem Schritt**: Bei jeder Handlungsanweisung, die eine Web-Seite betrifft
  (GitHub-Settings, Netlify-Dashboard, Drittanbieter-Tools etc.), IMMER den direkten
  Deep-Link zu genau der Seite/dem Schritt mitgeben. Nicht nur beschreiben, wo der
  Nutzer hinklicken soll, sondern den Link zum Anklicken liefern.
- Nutzer kommuniziert auf Deutsch.
- **KI-generierte Modelle, natürlich aber günstig**: Wenn beim Erstellen von Content
  KI-generierte Modelle/Personen zum Einsatz kommen (z. B. über Artlist oder Higgsfield),
  sollen diese natürlich und schön aussehen, aber nicht unnötig viele Tokens oder Kosten
  verursachen. Bei der Modellwahl also immer die günstigere/effizientere Option nehmen,
  solange die optische Qualität stimmt, nicht automatisch das teuerste Modell.

## Content-Agents (Instagram, YouTube, Reels)

Die Agents liegen in `.claude/agents/` und werden **über ihren Vornamen** angesprochen.
Sobald der Nutzer einen dieser Namen nennt, zum Beispiel "Sabine, erstell mir den
Beitrag zu Thema X", wird der passende Subagent per Agent-Tool gestartet.

| Name | Agent-Typ | Zuständig für |
|---|---|---|
| Sabine | `sabine` | Instagram Beiträge und Stories für Körperverwandlung, inkl. Caption |
| Sarah | `sarah` | Instagram Feed-Beiträge für Andreas Kotte (@andreas.kotte), keine Stories |
| Recherche Rita | `recherche-rita` | Themen- und Trendrecherche für Körperverwandlung |
| Recherche Robert | `recherche-robert` | Themen- und Trendrecherche für @andreas.kotte, Zielgruppe Unternehmer |
| Thumbnail Tom | `thumbnail-tom` | YouTube Titel und Thumbnail-Konzepte, immer 3 Varianten |
| Lisa | `lisa` | CapCut Schnitt-Prompts für Reels |
| Anna | `anna` | WhatsApp Channel Körperverwandlung, Postplan mit Datum je Nachricht |
| Peter | `peter` | Vieraugenprinzip, prüft Sabine, Sarah, Tom, Lisa und Anna vor dem Posten |

Typischer Ablauf: Rita oder Robert liefern Themen, Sabine oder Sarah bauen daraus
Beiträge, Peter prüft, dann wird gepostet. Anna läuft eigenständig für WhatsApp, sie
bekommt einen Zeitraum und liefert den kompletten Postplan.

`.claude/agents/GEMEINSAME-REGELN.md` gilt für alle acht Agents und steht über den
Einzelprofilen. Die zwei wichtigsten Regeln:

1. **Keine Strichzeichen statt Komma.** Kein `–`, kein `—`, kein freistehendes ` - `
   als Ersatz für Komma, Punkt oder Konjunktion. Bindestriche innerhalb von Wörtern
   bleiben erlaubt.
2. **Hand-Emojis immer mit Hautton** `🏼`, also 👋🏼 👍🏼 💪🏼 statt 👋 👍 💪.

Diese beiden Regeln gelten auch für alle normalen Antworten in diesem Projekt, nicht
nur für die Agents.

Zwei weitere Festlegungen aus den Gemeinsamen Regeln:

3. **Erstellen heißt rendern.** Sagt der Nutzer "erstell das", liefern Sabine, Sarah und
   Tom fertige Bilddateien, keine Textbeschreibung. Ablauf und Skript stehen in
   `.claude/agents/RENDERING.md`, das Story-Skript in
   `.claude/agents/scripts/story_slide.py`.
4. **Stories nur einmal.** Sabine baut die Story für Körperverwandlung, dieselben Slides
   werden 1:1 bei @andreas.kotte repostet. Sarah macht keine eigenen Stories.
5. **Peter läuft immer mit.** Sabine, Sarah und Tom rufen Peter selbst auf, bevor
   irgendetwas an den Nutzer geht, korrigieren seine Befunde selbst und liefern erst
   nach seiner Freigabe. Der Nutzer muss das nicht anfordern.
6. **Fragensticker eins zu eins.** Die Maße für den Instagram-Fragensticker stehen als
   Tabelle in `sabine.md` und als Konstanten in `scripts/story_slide.py`. Antwortkästen
   sind scharfkantig, die Sticker-Schrift ist eine neutrale Grotesk, nicht Decor.

## Kontakt
- E-Mail für Benachrichtigungen: andreaskotte@gmx.de

## Deployment

- Live-Seite (Reinigungs-Checkliste): https://radiant-youtiao-402f71.netlify.app
- Netlify-Projekt: radiant-youtiao-402f71
- Ziel: Netlify ist mit dem GitHub-Repo verbunden (Continuous Deployment), sodass
  jeder Git-Push auf `claude/cleaning-checklist-app-Xnsqk` automatisch deployt wird.
  Nutzer wünscht keinen manuellen Drag & Drop mehr.
