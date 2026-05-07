from sheets_airtable_sync.backbone import get_backbone_status, get_health


def test_backbone_status_is_fixture_safe() -> None:
    status = get_backbone_status()
    assert status.fixture_safe is True
    assert status.live_services_used is False
    assert status.synthetic_data_only is True


def test_health_has_sector_metadata() -> None:
    health = get_health()
    assert health["sector"] == "data-platform-sync"
    assert "airtable-upsert-preview" in health["capabilities"]
