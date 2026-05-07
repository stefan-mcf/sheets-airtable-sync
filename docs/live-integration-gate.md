# Live Integration Gate

Live integration is credible later, but not active in this repo.

Before any live run:

1. Create Google auth outside the repo: service account or OAuth with least-privilege Sheets scopes.
2. Confirm Google Sheets API v4 limits and 429 backoff behavior.
3. Create Airtable PAT/OAuth outside the repo with base/table-scoped access.
4. Confirm Airtable per-base rate limits and `Retry-After` handling.
5. Verify Airtable `performUpsert.mergeOnFields` against the exact live table schema.
6. Document webhook caveats: Airtable webhooks provide change notifications and require cursor payload retrieval plus renewal.
7. Use sandbox data first; never use client data without approval.

Current tests perform no provider network calls.
