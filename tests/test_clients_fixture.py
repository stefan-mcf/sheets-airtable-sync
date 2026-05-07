from sheets_airtable_sync.clients.fixture import FixtureSourceClient, FixtureTargetClient


def test_fixture_clients() -> None:
    rows = FixtureSourceClient(".").fetch_rows("examples/input/crm-leads.json")
    previews = FixtureTargetClient().preview_upserts(rows)
    assert rows and previews[0]["live_services_used"] is False
