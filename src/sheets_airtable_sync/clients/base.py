from __future__ import annotations

from typing import Any, Protocol


class SourceClient(Protocol):
    def fetch_rows(self, resource: str) -> list[dict[str, Any]]: ...


class TargetClient(Protocol):
    def preview_upserts(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]: ...
