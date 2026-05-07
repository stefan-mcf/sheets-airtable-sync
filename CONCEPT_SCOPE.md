# Sheets Airtable Sync — Concept and Scope

Date: 2026-05-05
Repo: sheets-airtable-sync
Visibility: public portfolio repository

## Concept pitch

Concrete proof project for spreadsheet/database automation: validate dirty rows, dedupe, normalize, create Airtable-style upserts, and produce a readable audit report.

The repo proves one workflow clearly: spreadsheet chaos can become a safe repeatable sync with rejected-row reasons, idempotent upsert previews, and handoff notes for integration platforms.

## Market signals addressed

Source: internal market research summaries, May 2026.

- API integration: 751 jobs / 39% in the demand landscape; API/REST appears as connective tissue across the market.
- AI/LLM workflow work: 673 jobs / 35%, strongest when framed as controlled workflow steps rather than vague agent claims.
- n8n/Make/Zapier workflow work: 593 jobs / 31%; Zapier, Make.com, and n8n repeatedly appear in premium and quick-win shortlists.
- Google Sheets automation: 199 jobs / 10% with strong hourly bands; Sheets work is boring but high-trust and easy to evaluate.
- Airtable build/automation: 273 jobs / 14%; Airtable + Make and Airtable + API requests recur in premium shortlists.
- Automation fix/debug: 119 jobs in the 168h mining report; strong early-review target because users are already in pain.
- GHL/HubSpot/CRM cluster: 279 jobs / 9.9% in the 168h mining report; high-volume wedge, even if average rates are lower.
- Slack/Discord bots: lower volume but high median niche; useful as an ops-notification proof surface.

Portfolio rule: each repo proves one buyer-legible outcome. Automation Kit remains the reusable local proof framework for running and validating automation patterns; this repository shows a concrete project implementation that can be evaluated on its own.

## Systems and workflows this repo makes visible

- Google Sheets
- Airtable
- Make.com
- Zapier
- Google Apps Script
- Shopify exports
- Google Ads/Meta Ads-style CSVs
- CRM rows

## Concrete proof flows

- Dirty lead rows -> accepted/rejected report -> Airtable-style upserts
- Shopify/ads export rows -> normalized reporting table
- Client/project tracker rows -> deduped operations table

## Evidence package

The implemented proof package includes:

- sample input fixtures;
- deterministic local runs;
- structured output JSON/CSV/reports;
- validation and audit-log evidence;
- operator-readable handoff notes;
- README with problem, solution, proof, and safety boundary;
- generated proof-panel screenshots;
- tests and validators that prove repeatability.

## Client-fit use

Best used when a workflow mentions any of these systems or patterns:

- Google Sheets
- Airtable
- Make.com
- Zapier
- Google Apps Script
- Shopify exports
- Google Ads/Meta Ads-style CSVs
- CRM rows

Representative first milestone:

> Validate and dedupe a sample export, produce accepted/rejected rows, and show the Airtable-ready upsert structure.

## Relationship to Automation Kit

- Automation Kit remains the reusable pattern library and local validation framework.
- This repo is a focused implementation/proof wrapper.
- It reuses Automation Kit-style vocabulary: workflow contract, fixtures, mock adapters, validation result, audit log, and handoff note.
- Companion proof repositories keep each portfolio link focused instead of overloading the reusable framework.

## Safety and scope boundaries

- Synthetic fixtures only in the committed proof package.
- Empty credential placeholders only.
- No live third-party service calls in the proof baseline.
- No customer-owned data in examples or evidence.
- No external message, platform submission, or off-repo delivery action.
- No cloud deployment, paid resource, or production-readiness claim.
- Evidence is deterministic: sample input, sample output, validation log, test output, and handoff notes.
