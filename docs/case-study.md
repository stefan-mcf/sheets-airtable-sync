# Case study: turning inconsistent spreadsheet rows into safe Airtable updates

Spreadsheets are often the easiest place for a team to start an operational process. They are also where inconsistent dates, duplicate contacts, missing identifiers, status variations, and manually formatted values accumulate.

When those rows are pushed directly into Airtable, the automation tends to fail in one of two ways: bad records are silently skipped, or the destination is updated without enough information to explain what changed.

Sheets Airtable Sync is a Python service that inserts a reviewable reconciliation stage between the spreadsheet and Airtable. It validates and normalises every row, detects duplicates, separates exceptions, and prepares deterministic upsert operations before any provider write occurs.

## The workflow

```text
spreadsheet-style rows
          │
          ▼
mapping configuration
          │
          ▼
field normalisation
          │
          ▼
validation and merge-key checks
          │
          ▼
deduplication
     ┌────┴─────┐
     ▼          ▼
upsert plan   rejected row
     │          │
     ▼          ▼
summary report  remediation note
```

The same reconciliation engine is available through a CLI, FastAPI endpoints, MCP-compatible functions, and an executor script for low-code or agent-driven handoff.

## Data scenarios

The repository includes six controlled datasets covering CRM leads, Shopify orders, Google Form responses, project tracking, mixed dirty rows, and Notion-style records. Four mapping configurations demonstrate how the engine adapts the same process to different operational schemas.

| Concern | Handling |
| --- | --- |
| Email and phone variation | Canonical normalisation before comparison |
| Dates and currency | Typed conversion with reason-coded failures |
| Status values | Mapping to an approved destination vocabulary |
| Multi-select values | Stable list normalisation |
| Duplicate records | Merge-key and idempotency checks |
| Missing merge keys | Rejected-row output with remediation guidance |

## Key engineering decisions

### Plan first, write later

The default operation is an upsert preview, not a provider update. It shows the exact Airtable-shaped fields, merge key, and idempotency value that would be used.

### Mapping rules are versionable

Source-to-destination rules live in JSON rather than being embedded in application code. A field rename or status change can be reviewed as a configuration diff.

### Rejected rows remain actionable

Invalid rows are not discarded. Each one receives a reason code, the affected field, and a remediation note so an operator can correct the source or approve a mapping change.

### Every surface uses the same engine

CLI commands, API endpoints, MCP functions, and the executor adapter all call the same validation and reconciliation logic. This avoids different outcomes depending on how the workflow is triggered.

## Result

The project delivers:

- reusable mapping and normalisation rules;
- deterministic upsert previews with stable merge keys;
- duplicate detection and idempotency identifiers;
- accepted, rejected, and dead-letter outputs;
- operator-readable Markdown reports;
- CLI, API, MCP, and executor access;
- Make, Zapier, n8n, and Apps Script handoff templates;
- 30 automated tests and screenshots generated from the committed scenarios.

The practical value is visibility before a bulk sync: the operator can see which records will update, which will stop, and why.

## Scope and production path

The committed datasets contain controlled local records. The default workflow does not authenticate to Google Sheets, Airtable, Notion, Make, Zapier, or n8n and does not update an external base.

The production path is documented separately and introduces read scopes, Airtable upsert permissions, rate-limit handling, retry policy, sandbox approval, and post-write readback. Those gates are intentionally separate from the reconciliation engine.

## Explore the implementation

- [Architecture](architecture.md)
- [API surface](api.md)
- [Platform handoff](platform-handoff.md)
- [Live integration gate](live-integration-gate.md)
- [Validation record](evidence.md)
- [Back to the repository overview](../README.md)
