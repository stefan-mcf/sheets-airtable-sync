import sys
from pathlib import Path

import pytest
from PIL import Image
from scripts.render_portfolio_images import public_text, run_cmd

EXPECTED_IMAGES = [
    "01-system-flow.png",
    "02-interface-surface.png",
    "03-core-processing.png",
    "04-guardrail-path.png",
    "05-output-readback.png",
    "06-validation-scope.png",
]


def test_portfolio_images_exist_and_are_readable_pngs() -> None:
    paths = sorted(Path("docs/screenshots").glob("*.png"))
    assert [path.name for path in paths] == EXPECTED_IMAGES
    for path in paths:
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(data) > 20_000
        with Image.open(path) as image:
            assert image.size == (1400, 800)
            assert image.info["ValidationStatus"] == "passed"
            public_copy = image.info["PortfolioCopy"]
            lowered = public_copy.lower()
            for term in ("pro" + "of", "evi" + "dence", "walk" + "through", "tuto" + "rial"):
                assert term not in lowered
            assert "/" + "Users/" not in public_copy
            assert "/" + "home/" not in public_copy


def test_portfolio_renderer_uses_current_sources() -> None:
    renderer = Path("scripts/render_portfolio_images.py").read_text()
    required_sources = [
        "examples/output/crm-leads-sync-report.json",
        "examples/output/dirty-rows-sync-report.json",
        "templates/make/airtable-upsert-scenario.json",
        "templates/zapier/sheets-to-airtable-zap.json",
        "templates/n8n/sheets-airtable-sync.workflow.json",
        "templates/gas/sheets-cleanup.gs",
    ]
    for source in required_sources:
        assert source in renderer

    required_commands = [
        '"-m", "pytest", "-q", "--disable-warnings"',
        '"-m", "ruff", "check", "."',
        '"-m", "mypy", "src"',
        '"scripts/verify_examples.py"',
        '"./executor.sh", "verify"',
    ]
    for command in required_commands:
        assert command in renderer

    assert renderer.index("generate_example_outputs()") < renderer.index("render_system_flow()")


def test_renderer_rejects_failed_commands() -> None:
    with pytest.raises(RuntimeError, match="command returned 7"):
        run_cmd([sys.executable, "-c", "raise SystemExit(7)"], timeout=10)


def test_public_text_removes_variable_command_timings() -> None:
    assert public_text("31 passed in 0.74s") == "31 passed"
