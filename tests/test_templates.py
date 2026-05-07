import json
from pathlib import Path


def test_json_templates_are_valid_and_fixture_safe() -> None:
    for path in Path("templates").rglob("*.json"):
        data = json.loads(path.read_text())
        assert data.get("live_services_used") is False


def test_gas_template_has_no_credentials() -> None:
    text = Path("templates/gas/sheets-cleanup.gs").read_text()
    assert "AIRTABLE_PAT" not in text
    assert "api_key" not in text.lower()
