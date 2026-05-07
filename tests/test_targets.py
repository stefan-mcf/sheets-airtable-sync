from sheets_airtable_sync.sync import run_scenario
from sheets_airtable_sync.targets import crm_upsert_preview, notion_page_preview


def test_target_payloads_are_preview_shapes() -> None:
    report = run_scenario("crm-leads")
    assert notion_page_preview(report)["live_services_used"] is False
    assert crm_upsert_preview(report)["contacts"]
