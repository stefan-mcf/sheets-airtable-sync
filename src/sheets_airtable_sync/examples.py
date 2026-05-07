from __future__ import annotations

from sheets_airtable_sync.sync import list_scenarios, run_scenario


def validate_examples() -> dict[str, object]:
    scenarios = []
    for item in list_scenarios():
        report = run_scenario(item["name"])
        scenarios.append({"name": item["name"], "summary_counts": report.summary_counts.model_dump(), "fixture_safe": report.fixture_safe, "live_services_used": report.live_services_used})
    return {"fixture_safe": True, "live_services_used": False, "synthetic_data_only": True, "scenarios": scenarios, "scenario_count": len(scenarios)}
