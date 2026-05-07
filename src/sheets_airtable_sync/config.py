from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sheets_airtable_sync.models import MappingConfig

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPPING = ROOT / "configs" / "mappings" / "leads-to-airtable.json"


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_mapping(path: str | Path = DEFAULT_MAPPING) -> MappingConfig:
    return MappingConfig.model_validate(load_json(path))


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    data = load_json(path)
    if isinstance(data, dict) and "rows" in data:
        rows = data["rows"]
    else:
        rows = data
    if not isinstance(rows, list):
        raise ValueError("input must be a JSON list or object with rows")
    return [dict(row) for row in rows]
