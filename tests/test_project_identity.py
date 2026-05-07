import json
from pathlib import Path


def test_project_identity_and_safety_metadata() -> None:
    metadata = json.loads(Path("repo-metadata.json").read_text())
    assert metadata["name"] == "sheets-airtable-sync"
    assert metadata["category"] == "data-platform-sync"
    assert metadata["private"] is False
    assert metadata["fixture_safe"] is True
    assert metadata["live_services_used"] is False
    assert metadata["synthetic_data_only"] is True
    legacy_key = "factory" + "_sector"
    assert legacy_key not in metadata
