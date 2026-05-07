# Sandbox Walkthrough

1. Validate fixtures: `PYTHONPATH=src python -m sheets_airtable_sync.cli validate-examples`.
2. Preview Airtable operations for a lane: `./executor.sh preview crm-leads`.
3. Render client-readable report: `./executor.sh report crm-leads`.
4. Inspect generated reports in `examples/output/`.
5. Use `docs/platform-handoff.md` to map the result into Make, Zapier, n8n, or GAS handoff language.

## Client adaptation matrix

| Client request | Fixture proof | Gated next step |
|---|---|---|
| Sheets -> Airtable | CRM leads fixture | confirm base schema |
| Forms -> Airtable | Google form responses | confirm form fields |
| Shopify export -> Airtable | Shopify orders fixture | confirm order columns |
| CRM cleanup | CRM leads fixture | confirm CRM export format |
| Notion-style backup | Notion rows fixture | confirm target schema |
| Ops notification | Slack/Discord mock payloads | approve webhook target |
