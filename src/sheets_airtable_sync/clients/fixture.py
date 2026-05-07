from __future__ import annotations

from pathlib import Path
from typing import Any

from sheets_airtable_sync.config import load_rows


class FixtureSourceClient:
    def __init__(self, root: Path | str = ".") -> None:
        self.root = Path(root)

    def fetch_rows(self, resource: str) -> list[dict[str, Any]]:
        return load_rows(self.root / resource)


class FixtureTargetClient:
    def preview_upserts(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{"operation": "fixture_upsert_preview", "fields": row, "live_services_used": False} for row in rows]
