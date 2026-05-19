# Projektnotizen für Claude

## Nutzer-Präferenzen

- **Klickbare Links**: Wenn der Nutzer eine Web-Seite, App oder ein Tool erstellt bekommt,
  IMMER einen direkten klickbaren Hyperlink in der Antwort ausgeben, mit dem die
  Anwendung sofort im Browser geöffnet werden kann (z. B. via raw.githack.com,
  GitHub Pages, Vercel-Preview o. ä.). Nicht nur erklären, wie man sie deployt —
  einen funktionierenden Link liefern.
- **URL bei jedem Schritt**: Bei jeder Handlungsanweisung, die eine Web-Seite betrifft
  (GitHub-Settings, Netlify-Dashboard, Drittanbieter-Tools etc.), IMMER den direkten
  Deep-Link zu genau der Seite/dem Schritt mitgeben. Nicht nur beschreiben, wo der
  Nutzer hinklicken soll — den Link zum Anklicken liefern.
- Nutzer kommuniziert auf Deutsch.

## Kontakt
- E-Mail für Benachrichtigungen: andreaskotte@gmx.de

## Deployment

- Live-Seite (Reinigungs-Checkliste): https://radiant-youtiao-402f71.netlify.app
- Netlify-Projekt: radiant-youtiao-402f71
- Ziel: Netlify ist mit dem GitHub-Repo verbunden (Continuous Deployment), sodass
  jeder Git-Push auf `claude/cleaning-checklist-app-Xnsqk` automatisch deployt wird.
  Nutzer wünscht keinen manuellen Drag & Drop mehr.
