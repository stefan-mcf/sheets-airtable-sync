# Case Study: Spreadsheet-to-Airtable Sync Cleanup

## Client problem

Small teams often run operations in Sheets while their database of record lives in Airtable. Dirty rows, duplicate leads/orders, inconsistent dates, invalid emails, and missing merge keys make low-code automations fragile.

## Proof flow

1. Load synthetic buyer-shaped rows from `examples/input/`.
2. Apply a JSON mapping from `configs/mappings/`.
3. Normalize fields and reject unsafe or invalid values.
4. Dedupe by stable merge key.
5. Emit Airtable-shaped upsert previews, dead letters, and reports.
6. Expose the same engine through CLI, FastAPI, MCP functions, and `executor.sh`.

## Automation Kit relationship

Automation Kit remains the shared runtime vocabulary. This repo is the data-platform-sync sector proof with an optional backbone detector.

## Safety boundary

No live provider accounts, credentials, cloud deployment, or client data are used. Live implementation would require a separate credential/sandbox gate.
