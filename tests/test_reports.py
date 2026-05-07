from sheets_airtable_sync.reports import report_to_html, report_to_json, report_to_markdown
from sheets_airtable_sync.sync import run_scenario


def test_reports_render_all_formats() -> None:
    report = run_scenario("crm-leads")
    assert "Sync Report" in report_to_markdown(report)
    assert "<!doctype html>" in report_to_html(report)
    assert '"fixture_safe": true' in report_to_json(report)
