# Sheets Airtable Sync Plan

This public root plan summarizes the implemented fixture-safe data-platform-sync proof.

Detailed local execution plans may exist under `docs/plans/`, but that folder is intentionally ignored so private operator paths and research notes do not enter the public surface.

Implemented public scope:

- synthetic fixture families and mapping configs;
- typed validation, normalization, dedupe, dead-letter, idempotency, and Airtable upsert-preview contracts;
- CLI, local FastAPI, MCP tool functions, and `executor.sh` adapter;
- Make, Zapier, n8n, and Google Apps Script handoff templates;
- generated reports and proof-panel screenshots;
- Docker/local deployment checkpoint;
- local verification gates and public-readiness documentation.

Safety boundary: synthetic fixtures only, no live Google Sheets, Airtable, Make, Zapier, n8n, Notion, Slack, Discord, CRM, cloud deployment, release/tag, external-submission action, or customer-owned data without separate explicit approval.
