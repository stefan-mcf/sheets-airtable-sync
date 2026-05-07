from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def make_merge_key(fields: dict[str, Any], merge_key_fields: list[str]) -> str:
    parts = []
    for field in merge_key_fields:
        value = fields.get(field, "")
        if isinstance(value, list):
            value = ",".join(str(v).lower().strip() for v in value)
        parts.append(str(value or "").lower().strip())
    return "|".join(parts) if any(parts) else stable_hash(fields)


def make_idempotency_key(scenario: str, merge_key: str, fields: dict[str, Any]) -> str:
    return f"{scenario}:{merge_key}:{stable_hash(fields)}"
