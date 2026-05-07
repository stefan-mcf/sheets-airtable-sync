# Local Deployment

Build local container proof:

```bash
docker build -t sheets-airtable-sync .
docker run --rm sheets-airtable-sync ./executor.sh verify
```

API mode with Compose:

```bash
docker compose up --build sheets-airtable-sync-api
curl -fsS http://127.0.0.1:8014/health
docker compose down
```

No cloud resource is required. Environment variables are empty placeholders unless a later live gate is approved.
