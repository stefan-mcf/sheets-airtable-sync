from sheets_airtable_sync.dead_letter import build_rejected
from sheets_airtable_sync.models import ReasonCode


def test_dead_letter_shape() -> None:
    row = build_rejected(1, "scenario", ReasonCode.MISSING_REQUIRED_FIELD, {"x": ""}, "x")
    assert row.reason_code == ReasonCode.MISSING_REQUIRED_FIELD
    assert row.suggested_remediation
