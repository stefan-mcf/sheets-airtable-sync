# Portfolio Review Checkpoint

Status: local fixture-safe implementation ready for public-readiness audit and private push review.

Gates still requiring explicit approval:

- Git push or remote mutation.
- GitHub visibility change.
- Release/tag/public export.
- Live Google Sheets/Airtable or other provider credentials.
- Cloud deployment.
- Customer-owned data.
- External buyer/operator message submission.

Verification should be refreshed before any push:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m ruff check .
PYTHONPATH=src python -m mypy src
python scripts/verify_examples.py
./executor.sh verify
git diff --check
```
