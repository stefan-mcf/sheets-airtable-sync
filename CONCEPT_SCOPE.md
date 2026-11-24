# Sheets Airtable Sync scope

Sheets Airtable Sync reconciles spreadsheet-shaped fixture rows into an Airtable upsert plan for operator review.

- Applies a typed mapping, validates fields and formula cells, and normalises values.
- Derives stable merge keys and records reasons for invalid or duplicate rows.
- Produces deterministic Airtable-shaped upsert previews and reconciliation reports for leads, orders, reporting exports and operations records.

The CLI, FastAPI and MCP interfaces share the preview contract. The committed scenarios use synthetic inputs and run without live Google Sheets or Airtable calls. See [local operation](docs/local-operation.md), [architecture](docs/architecture.md) and the [live integration gate](docs/live-integration-gate.md).
