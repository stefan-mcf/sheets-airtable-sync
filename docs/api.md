# Local API

Run locally:

```bash
PYTHONPATH=src python -m uvicorn sheets_airtable_sync.api:app --host 127.0.0.1 --port 8014
```

Endpoints:

- `GET /health`
- `GET /examples`
- `POST /sync/preview`
- `POST /reports/render`
- `POST /mappings/validate`

Example:

```bash
curl -fsS -X POST http://127.0.0.1:8014/sync/preview \
  -H 'Content-Type: application/json' \
  --data @examples/api-requests/sync-preview-request.json
```

All responses include fixture safety flags and use local files only.
