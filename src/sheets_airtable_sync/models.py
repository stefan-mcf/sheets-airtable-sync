from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ReasonCode(str, Enum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    INVALID_EMAIL = "invalid_email"
    INVALID_DATE = "invalid_date"
    INVALID_CURRENCY = "invalid_currency"
    DUPLICATE_MERGE_KEY = "duplicate_merge_key"
    UNSAFE_FORMULA_CELL = "unsafe_formula_cell"
    LINKED_RECORD_UNRESOLVED = "linked_record_unresolved"
    MAPPING_FIELD_MISSING = "mapping_field_missing"
    TYPE_MISMATCH = "type_mismatch"
    CONFLICT_BOTH_CHANGED = "conflict_both_changed"
    RATE_LIMIT_RETRY_EXHAUSTED = "rate_limit_retry_exhausted"


class SafetyModel(BaseModel):
    fixture_safe: bool = True
    live_services_used: bool = False
    synthetic_data_only: bool = True


class SourceRow(BaseModel):
    model_config = ConfigDict(extra="allow")
    row_number: int | None = None
    scenario: str | None = None


class NormalizedRow(SafetyModel):
    row_number: int
    scenario: str
    merge_key: str
    fields: dict[str, Any]


class RejectedRow(BaseModel):
    row_number: int
    scenario: str
    reason_code: ReasonCode
    reason: str
    original: dict[str, Any]
    suggested_remediation: str


class DuplicateRow(BaseModel):
    row_number: int
    scenario: str
    merge_key: str
    original: dict[str, Any]
    reason_code: ReasonCode = ReasonCode.DUPLICATE_MERGE_KEY


class AirtableUpsertOperation(SafetyModel):
    system: Literal["airtable"] = "airtable"
    operation: Literal["upsert"] = "upsert"
    record_id: str
    merge_on_fields: list[str]
    idempotency_key: str
    fields: dict[str, Any]


class SyncAuditEvent(BaseModel):
    row_number: int
    scenario: str
    decision: Literal["accepted", "rejected", "duplicate", "conflict"]
    reason_code: str | None = None
    live_services_used: bool = False


class SyncSummaryCounts(BaseModel):
    accepted: int = 0
    rejected: int = 0
    duplicates: int = 0
    conflicts: int = 0
    upserts: int = 0


class FieldMapping(BaseModel):
    source_field: str
    target_field: str
    transform: str = "text"
    required: bool = False
    default: Any = None
    empty_policy: Literal["keep", "default", "reject", "drop"] = "keep"
    merge_key: bool = False


class MappingConfig(BaseModel):
    scenario: str
    description: str = ""
    merge_key_fields: list[str] = Field(default_factory=list)
    duplicate_policy: Literal["first_wins", "last_wins", "reject"] = "first_wins"
    conflict_policy: Literal["report_only", "source_wins", "target_wins"] = "report_only"
    fields: list[FieldMapping]


class SyncReport(SafetyModel):
    scenario: str
    summary_counts: SyncSummaryCounts
    accepted_rows: list[NormalizedRow]
    rejected_rows: list[RejectedRow]
    duplicate_rows: list[DuplicateRow]
    airtable_upserts: list[AirtableUpsertOperation]
    audit_log: list[SyncAuditEvent]
    handoff_notes: str
    risk_notes: list[str] = Field(default_factory=list)
