# Platform Handoff Templates

Templates under `templates/` show familiarity with Make, Zapier, n8n, and Google Apps Script without importing anything into live accounts.

- Make: watch row -> local preview API -> Airtable upsert preview -> notification preview.
- Zapier: Sheets/Form trigger -> Formatter -> local webhook/API -> Airtable-shaped output.
- n8n: schedule/webhook -> local API -> transformed data -> notification.
- GAS: lightweight cleanup script for client-owned Sheets.

All templates are fixtures and contain no credentials.
