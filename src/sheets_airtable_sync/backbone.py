from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.util import find_spec
from typing import Any


@dataclass(frozen=True)
class BackboneStatus:
    automation_kit_available: bool
    fixture_safe: bool = True
    live_services_used: bool = False
    synthetic_data_only: bool = True

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SectorMetadata:
    sector: str = "data-platform-sync"
    package: str = "sheets-airtable-sync"
    capabilities: tuple[str, ...] = (
        "schema-validation",
        "row-normalization",
        "dedupe",
        "airtable-upsert-preview",
        "dead-letter-reporting",
        "local-api",
        "mcp-tools",
        "executor-adapter",
    )

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["capabilities"] = list(self.capabilities)
        return data


def get_backbone_status() -> BackboneStatus:
    return BackboneStatus(automation_kit_available=find_spec("automation_kit") is not None or find_spec("auto_kit") is not None)


def get_health() -> dict[str, Any]:
    status = get_backbone_status().as_dict()
    status.update(SectorMetadata().as_dict())
    return status
