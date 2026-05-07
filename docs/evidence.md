# Evidence

Run the local gate:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m ruff check .
PYTHONPATH=src python -m mypy src
python scripts/verify_examples.py
./executor.sh verify
```

Evidence package:

- CLI: `examples/cli/README.md`
- API requests: `examples/api-requests/`
- API responses: `examples/api-responses/`
- MCP: `examples/mcp/`
- reports: `examples/output/`
- proof panels: `docs/screenshots/`
- platform templates: `templates/`

Proof panel generation:

- `scripts/render_proof_screenshots.py` reads committed JSON reports and API responses.
- It embeds actual scenario counts, accepted/rejected rows, duplicate keys, reason codes, idempotency keys, and template excerpts.
- It executes representative CLI commands and local quality gates while rendering, so failures appear in the screenshots instead of static placeholder cards.
- `tests/test_screenshots.py` verifies the PNG package and checks that the renderer is wired to real evidence sources and gate commands.

Safety: all evidence is generated from synthetic local fixtures and records `live_services_used=false`.
