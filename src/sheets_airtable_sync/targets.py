from __future__ import annotations

from typing import Any

from sheets_airtable_sync.models import SyncReport


def notion_page_preview(report: SyncReport) -> dict[str, Any]:
    return {"object": "page", "parent": {"database_id": "mock_database_id"}, "properties": {"Name": {"title": [{"text": {"content": f"{report.scenario} sync summary"}}]}, "Status": {"select": {"name": "Fixture Preview"}}}, "fixture_safe": True, "live_services_used": False}


def crm_upsert_preview(report: SyncReport) -> dict[str, Any]:
    contacts = []
    for op in report.airtable_upserts:
        contacts.append({"external_id": op.idempotency_key, "properties": op.fields})
    return {"target": "generic-crm", "operation": "upsert_contacts", "contacts": contacts, "fixture_safe": True, "live_services_used": False}
