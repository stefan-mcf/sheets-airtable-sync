from __future__ import annotations

from typing import Any

from sheets_airtable_sync.models import SyncReport


def slack_payload(report: SyncReport) -> dict[str, Any]:
    c = report.summary_counts
    return {"channel": "#automation-fixture", "text": f"Sheets/Airtable fixture preview: {c.accepted} accepted, {c.rejected} rejected, {c.duplicates} duplicates.", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": f"*{report.scenario}* fixture-safe sync preview complete."}}], "fixture_safe": True, "live_services_used": False}


def discord_payload(report: SyncReport) -> dict[str, Any]:
    c = report.summary_counts
    return {"username": "automation-fixture-bot", "content": f"{report.scenario}: {c.upserts} Airtable upsert previews, {c.rejected} rejected rows.", "fixture_safe": True, "live_services_used": False}
