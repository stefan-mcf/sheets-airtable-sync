from sheets_airtable_sync.notifications import discord_payload, slack_payload
from sheets_airtable_sync.sync import run_scenario


def test_notification_payloads_are_mock_only() -> None:
    report = run_scenario("crm-leads")
    assert slack_payload(report)["live_services_used"] is False
    assert discord_payload(report)["fixture_safe"] is True
