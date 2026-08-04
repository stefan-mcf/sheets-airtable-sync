# Validation

Run the local gate:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m ruff check .
PYTHONPATH=src python -m mypy src
python scripts/verify_examples.py
./executor.sh verify
```

Validation surfaces:

- CLI: `examples/cli/README.md`
- API requests: `examples/api-requests/`
- API responses: `examples/api-responses/`
- MCP: `examples/mcp/`
- reports: `examples/output/`
- portfolio images: `docs/screenshots/`
- platform templates: `templates/`

Portfolio image generation:

- `scripts/render_portfolio_images.py` regenerates ignored scenario outputs before reading them, so a clean checkout has a deterministic source order.
- It embeds actual scenario counts, accepted/rejected rows, duplicate keys, reason codes, idempotency keys, and template excerpts.
- It stops immediately when a representative command or local quality gate returns a non-zero status.
- `tests/test_screenshots.py` verifies the six-image package and checks that the renderer is wired to current sources and gate commands.

Safety: all generated material uses synthetic local fixtures and records `live_services_used=false`.
