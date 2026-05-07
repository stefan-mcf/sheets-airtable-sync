from __future__ import annotations

from sheets_airtable_sync.sync import sync_rows


def test_dirty_rows_are_normalized_deduped_and_reported() -> None:
    rows = [
        {
            "customer_name": " Alice Ng ",
            "email": "ALICE@example.com",
            "company": "Northwind",
            "status": "New",
            "estimated_value": "1000",
        },
        {
            "customer_name": "Alice Ng",
            "email": "alice@example.com",
            "company": "Northwind",
            "status": "new",
            "estimated_value": "1000",
        },
        {"customer_name": "No Email", "email": "", "company": "Acme", "status": "active"},
    ]

    result = sync_rows(rows)

    assert result["summary_counts"] == {"accepted": 1, "rejected": 1, "duplicates": 1, "upserts": 1}
    assert result["accepted_rows"][0]["email"] == "alice@example.com"
    assert result["accepted_rows"][0]["status"] == "new"
    assert result["duplicate_rows"][0]["email"] == "alice@example.com"
    assert result["rejected_rows"][0]["reason"] == "missing_required_field: email"
    assert result["airtable_upserts"][0]["record_id"] == "lead:alice@example.com"
    assert result["live_services_used"] is False


def test_company_and_name_dedupe_when_email_missing_but_rejects_after_reason() -> None:
    rows = [
        {"customer_name": "Bob", "email": "", "company": "Acme", "status": "new"},
        {"customer_name": "Bob", "email": "", "company": "Acme", "status": "new"},
    ]

    result = sync_rows(rows)

    assert len(result["rejected_rows"]) == 1
    assert len(result["duplicate_rows"]) == 1
    assert result["airtable_upserts"] == []
