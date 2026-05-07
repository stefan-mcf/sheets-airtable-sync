# Architecture

Sheets Airtable Sync is a fixture-safe data-platform-sync proof. It stays thin: synthetic spreadsheet-like inputs flow through mapping configuration, validation, normalization, dedupe, dead-letter classification, Airtable-shaped upsert previews, and deterministic reports.

```text
fixtures -> mapping config -> sync engine -> reports/API/MCP/executor -> proof panels
```

Automation Kit remains the reusable backbone. This repo exposes a sibling-compatible optional `BackboneStatus` and never requires Automation Kit to be installed for local proof execution.

## Boundaries

- Fixture rows only by default.
- No Google Sheets, Airtable, Notion, Slack, Discord, CRM, Make, Zapier, n8n, or cloud network calls in tests or examples.
- Live clients are placeholders behind `docs/live-integration-gate.md`.
