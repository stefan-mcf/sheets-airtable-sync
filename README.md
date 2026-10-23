# Sheets Airtable Sync

Google Sheets to Airtable reconciliation service for validating, normalising, deduplicating, and planning record updates before a provider write.

**Status:** an SM Systems reference implementation; the included scenarios produce local upsert previews.

**My contribution:** reconciliation design, normalisation, validation, CLI/API interfaces and operating reports.

[Case study](docs/case-study.md) | [Architecture](docs/architecture.md) | [Local operation](docs/local-operation.md)

![Generated local processing example](docs/screenshots/03-core-processing.png)

*Generated panel from synthetic local scenarios. Further views are in the [image index](docs/screenshots/README.md); recorded totals are separate from current CI.*

## How it works

The service turns inconsistent spreadsheet rows into Airtable-ready upsert previews, rejected-row output, readable reports, and operator-accessible interfaces. It is designed for teams that need predictable data cleanup and a controlled handoff before changing a live base.

1. Load a mapping and spreadsheet-shaped input.
2. Validate required fields and reject unsafe formula cells.
3. Normalise typed values and derive the merge key.
4. Separate duplicates and invalid rows with reason codes.
5. Prepare idempotent Airtable upsert operations.
6. Return JSON, Markdown, HTML, API, or MCP output for operator review.

CLI, FastAPI and MCP interfaces share the preview contract. See the [interface documentation](docs/api.md) for supported calls.

## Usage

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
PYTHONPATH=src python -m sheets_airtable_sync.cli health --json
PYTHONPATH=src python -m sheets_airtable_sync.cli validate-examples
```

Start the local API:

```bash
PYTHONPATH=src python -m uvicorn sheets_airtable_sync.api:app --host 127.0.0.1 --port 8014
curl -fsS http://127.0.0.1:8014/health
curl -fsS -X POST http://127.0.0.1:8014/sync/preview \
  -H 'Content-Type: application/json' \
  --data @examples/api-requests/sync-preview-request.json
```

## Validation

```bash
PYTHONPATH=src python -m pytest -q
python -m ruff check .
PYTHONPATH=src python -m mypy src
python scripts/verify_examples.py
./executor.sh verify
PYTHONPATH=src python scripts/render_portfolio_images.py
```

## Scope and current state

Committed scenarios use synthetic data and empty credential placeholders. No live Google Sheets, Airtable, CRM, Notion, Slack, Discord, Make, Zapier, n8n, cloud, payment, delivery, client-data, or external-submission action runs by default.

Live Google Sheets and Airtable operation requires separately approved credentials, target-schema confirmation, provider rate-limit handling, and a sandbox run. See [the live integration gate](docs/live-integration-gate.md).

## Documentation

- [Validation record](docs/validation.md)
- [API contract](docs/api.md)
- [MCP contract](docs/mcp.md)
- [Executor contract](docs/executor.md)
- [Platform handoff](docs/platform-handoff.md)
- [Live integration gate](docs/live-integration-gate.md)
- [Image index](docs/screenshots/README.md)

MIT. See [LICENSE](LICENSE).
