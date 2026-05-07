# Client Adaptation Matrix

| Buyer phrase | Proof artifact | First milestone | Gated next step |
|---|---|---|---|
| Airtable + Make | `templates/make/` | fixture scenario blueprint | import into client Make only after approval |
| Google Sheets + GAS | `templates/gas/sheets-cleanup.gs` | cleanup trigger sample | bind to client Sheet after approval |
| CRM/GHL/HubSpot import cleanup | `examples/input/crm-leads.json` | normalize/dedupe report | map exact export headers |
| Shopify order table cleanup | `examples/input/shopify-orders.json` | order upsert preview | confirm order schema |
| Notion database migration | `examples/input/notion-database-rows.json` | target-shaped preview | approve Notion API use |
| Discord/Slack ops notification | `examples/output/*notification.json` | mock summary payload | approve webhook target |
