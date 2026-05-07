from __future__ import annotations

from typing import Any

from sheets_airtable_sync.models import ReasonCode, RejectedRow

REMEDIATIONS: dict[ReasonCode, str] = {
    ReasonCode.MISSING_REQUIRED_FIELD: "Fill the required source field or change the mapping to optional.",
    ReasonCode.INVALID_EMAIL: "Correct the email address before retrying the row.",
    ReasonCode.INVALID_DATE: "Use ISO date format YYYY-MM-DD or a configured date parser.",
    ReasonCode.INVALID_CURRENCY: "Use a numeric amount without ambiguous text.",
    ReasonCode.UNSAFE_FORMULA_CELL: "Replace spreadsheet formulas with literal values before export.",
    ReasonCode.MAPPING_FIELD_MISSING: "Add the source column to the fixture or adjust the mapping config.",
    ReasonCode.TYPE_MISMATCH: "Align the source value with the target Airtable field type.",
    ReasonCode.LINKED_RECORD_UNRESOLVED: "Resolve the linked record reference in a separate lookup step.",
    ReasonCode.CONFLICT_BOTH_CHANGED: "Review source and target changes before applying a live update.",
    ReasonCode.RATE_LIMIT_RETRY_EXHAUSTED: "Wait for the provider retry window and retry the batch.",
    ReasonCode.DUPLICATE_MERGE_KEY: "Review duplicate merge keys and keep only the intended winner.",
}


def build_rejected(row_number: int, scenario: str, code: ReasonCode, original: dict[str, Any], detail: str = "") -> RejectedRow:
    return RejectedRow(
        row_number=row_number,
        scenario=scenario,
        reason_code=code,
        reason=f"{code.value}{(': ' + detail) if detail else ''}",
        original=original,
        suggested_remediation=REMEDIATIONS[code],
    )
