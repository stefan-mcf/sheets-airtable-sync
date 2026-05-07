from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from email.utils import parseaddr
from typing import Any

from sheets_airtable_sync.models import ReasonCode


def norm_text(value: object) -> str:
    return str(value or "").strip()


def norm_email(value: object) -> str:
    email = norm_text(value).lower()
    parsed = parseaddr(email)[1]
    if parsed and "@" in parsed:
        return parsed
    return email


def norm_status(value: object) -> str:
    status = norm_text(value).lower().replace("_", "-").replace(" ", "-")
    aliases = {"": "new", "new-lead": "new", "todo": "todo", "in-progress": "active", "won": "active", "closed-won": "active"}
    return aliases.get(status, status or "new")


def norm_bool(value: object) -> bool | None:
    if value is None or norm_text(value) == "":
        return None
    return norm_text(value).lower() in {"1", "true", "yes", "y", "done", "paid"}


def norm_currency(value: object) -> str:
    text = norm_text(value).replace("$", "").replace(",", "")
    if text == "":
        return ""
    try:
        return str(Decimal(text).quantize(Decimal("0.01")))
    except InvalidOperation as exc:
        raise ValueError(ReasonCode.INVALID_CURRENCY.value) from exc


def norm_number(value: object) -> int | float | str:
    text = norm_text(value).replace(",", "")
    if text == "":
        return ""
    try:
        number = float(text)
    except ValueError:
        return text
    return int(number) if number.is_integer() else number


def norm_date(value: object) -> str:
    text = norm_text(value)
    if not text:
        return ""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError as exc:
        raise ValueError(ReasonCode.INVALID_DATE.value) from exc


def norm_phone(value: object) -> str:
    return "".join(ch for ch in norm_text(value) if ch.isdigit() or ch == "+")


def norm_multiselect(value: object) -> list[str]:
    if isinstance(value, list):
        return [norm_text(v) for v in value if norm_text(v)]
    return [part.strip() for part in norm_text(value).replace(";", ",").split(",") if part.strip()]


def guard_formula(value: Any) -> None:
    if isinstance(value, str) and value.strip().startswith(("=", "+", "-", "@")):
        raise ValueError(ReasonCode.UNSAFE_FORMULA_CELL.value)


def apply_transform(value: Any, transform: str) -> Any:
    guard_formula(value)
    transforms = {
        "text": norm_text,
        "email": norm_email,
        "status": norm_status,
        "date": norm_date,
        "datetime": norm_date,
        "currency": norm_currency,
        "number": norm_number,
        "boolean": norm_bool,
        "bool": norm_bool,
        "phone": norm_phone,
        "select": norm_text,
        "multi_select": norm_multiselect,
        "multiselect": norm_multiselect,
    }
    return transforms.get(transform, norm_text)(value)
