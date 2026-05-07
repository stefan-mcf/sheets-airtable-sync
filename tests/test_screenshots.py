from pathlib import Path

from PIL import Image


def test_screenshots_exist_and_are_readable_pngs() -> None:
    paths = sorted(Path("docs/screenshots").glob("*.png"))
    assert len(paths) >= 8
    for path in paths:
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(data) > 20_000
        with Image.open(path) as image:
            assert image.size[0] >= 1400
            assert image.size[1] >= 850


def test_screenshot_renderer_uses_real_evidence_sources() -> None:
    renderer = Path("scripts/render_proof_screenshots.py").read_text()
    required_sources = [
        "examples/output/crm-leads-sync-report.json",
        "examples/output/dirty-rows-sync-report.json",
        "examples/api-responses/sync-preview-response.json",
        "templates/make/airtable-upsert-scenario.json",
        "templates/zapier/sheets-to-airtable-zap.json",
        "templates/n8n/sheets-airtable-sync.workflow.json",
        "templates/gas/sheets-cleanup.gs",
    ]
    for source in required_sources:
        assert source in renderer

    required_commands = [
        '"-m", "pytest", "-q"',
        '"-m", "ruff", "check", "."',
        '"-m", "mypy", "src"',
        '"scripts/verify_examples.py"',
        '"./executor.sh", "verify"',
    ]
    for command in required_commands:
        assert command in renderer
