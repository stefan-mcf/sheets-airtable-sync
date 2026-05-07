from sheets_airtable_sync.mcp_server import (
    get_sheets_airtable_health,
    list_sheets_airtable_scenarios,
    plan_airtable_upserts,
    render_sync_report,
    validate_sheets_airtable_rows,
)


def test_mcp_tool_functions_are_fixture_safe() -> None:
    assert get_sheets_airtable_health()["fixture_safe"] is True
    assert list_sheets_airtable_scenarios()
    validation = validate_sheets_airtable_rows("examples/input/crm-leads.json", "configs/mappings/leads-to-airtable.json")
    assert validation["live_services_used"] is False
    upserts = plan_airtable_upserts("examples/input/crm-leads.json", "configs/mappings/leads-to-airtable.json")
    assert upserts["airtable_upserts"]
    assert "Sync Report" in render_sync_report("crm-leads")["content"]
