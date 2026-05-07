# Executor Adapter

`executor.sh` gives agents and operators a predictable shell contract:

```bash
./executor.sh health
./executor.sh validate crm-leads
./executor.sh preview crm-leads
./executor.sh report crm-leads
./executor.sh api-smoke
./executor.sh verify
```

The adapter refuses live mode unless both `SHEETS_AIRTABLE_SYNC_LIVE_SERVICES=true` and `SHEETS_AIRTABLE_SYNC_EXPLICIT_LIVE_APPROVAL=true` are set. Even then, this repo currently contains only fixture/stub clients.
