from sheets_airtable_sync.examples import validate_examples
from sheets_airtable_sync.sync import list_scenarios, run_scenario


def test_all_examples_validate_without_live_services() -> None:
    result = validate_examples()
    assert result["scenario_count"] >= 5
    for item in result["scenarios"]:
        assert item["fixture_safe"] is True
        assert item["live_services_used"] is False


def test_scenarios_have_expected_counts() -> None:
    names = {item["name"] for item in list_scenarios()}
    assert {"crm-leads", "shopify-orders", "project-tracker", "google-form-responses"}.issubset(names)
    assert run_scenario("crm-leads").summary_counts.upserts >= 2
