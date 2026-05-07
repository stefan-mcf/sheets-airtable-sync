from fastapi.testclient import TestClient

from sheets_airtable_sync.api import app

client = TestClient(app)


def test_api_health_and_examples() -> None:
    assert client.get("/health").json()["fixture_safe"] is True
    assert client.get("/examples").json()["examples"]


def test_api_preview_report_and_mapping() -> None:
    payload = {"input_path": "examples/input/crm-leads.json", "mapping_path": "configs/mappings/leads-to-airtable.json"}
    preview = client.post("/sync/preview", json=payload)
    assert preview.status_code == 200
    assert preview.json()["summary_counts"]["upserts"] >= 2
    report = client.post("/reports/render", json=payload | {"format": "md"})
    assert "Sync Report" in report.json()["content"]
    mapping = client.post("/mappings/validate", json={"mapping_path": "configs/mappings/leads-to-airtable.json"})
    assert mapping.json()["ok"] is True
