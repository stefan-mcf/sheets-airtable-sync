# Portfolio Review Checkpoint

Status: public fixture-safe implementation with CI-backed public baseline.

## Current public state

- GitHub repo: <https://github.com/stefan-mcf/sheets-airtable-sync>
- Visibility: public.
- Role: Google Sheets/Airtable-style validation, dedupe, mock upsert, rejected-row reporting, and audit-log proof spoke.
- CI workflow: `.github/workflows/ci.yml` present and latest public baseline has green CI.

## Remaining gates

- Release/tag/public product launch.
- Live Google Sheets/Airtable or other provider credentials.
- Cloud deployment.
- Customer-owned data.
- External buyer/operator message submission.

## Verification bundle

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m ruff check .
PYTHONPATH=src python -m mypy src
python scripts/verify_examples.py
./executor.sh verify
git diff --check
```
