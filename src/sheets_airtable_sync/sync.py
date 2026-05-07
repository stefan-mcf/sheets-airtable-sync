from __future__ import annotations

from pathlib import Path
from typing import Any

from sheets_airtable_sync.config import DEFAULT_MAPPING, load_mapping, load_rows
from sheets_airtable_sync.dead_letter import build_rejected
from sheets_airtable_sync.idempotency import make_idempotency_key, make_merge_key
from sheets_airtable_sync.models import (
    AirtableUpsertOperation,
    DuplicateRow,
    FieldMapping,
    MappingConfig,
    NormalizedRow,
    ReasonCode,
    SyncAuditEvent,
    SyncReport,
    SyncSummaryCounts,
)
from sheets_airtable_sync.transforms import apply_transform, norm_email, norm_text

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS: dict[str, tuple[str, str]] = {
    "dirty-rows": ("examples/input/dirty-rows.json", "configs/mappings/leads-to-airtable.json"),
    "crm-leads": ("examples/input/crm-leads.json", "configs/mappings/leads-to-airtable.json"),
    "shopify-orders": ("examples/input/shopify-orders.json", "configs/mappings/shopify-orders-to-airtable.json"),
    "project-tracker": ("examples/input/project-tracker.json", "configs/mappings/project-tracker-to-airtable.json"),
    "google-form-responses": ("examples/input/google-form-responses.json", "configs/mappings/form-responses-to-airtable.json"),
    "notion-database-rows": ("examples/input/notion-database-rows.json", "configs/mappings/project-tracker-to-airtable.json"),
}


def list_scenarios() -> list[dict[str, str]]:
    return [{"name": name, "input": inp, "mapping": mapping} for name, (inp, mapping) in SCENARIOS.items()]


def _legacy_mapping() -> MappingConfig:
    return MappingConfig(
        scenario="legacy-leads",
        description="Compatibility mapping for sync_rows(rows)",
        merge_key_fields=["Email"],
        fields=[
            FieldMapping(source_field="customer_name", target_field="Name", transform="text", required=True),
            FieldMapping(source_field="email", target_field="Email", transform="email", required=True, merge_key=True),
            FieldMapping(source_field="company", target_field="Company", transform="text"),
            FieldMapping(source_field="status", target_field="Status", transform="status", default="new"),
            FieldMapping(source_field="estimated_value", target_field="Estimated Value", transform="currency"),
        ],
    )


def sync_rows_with_mapping(rows: list[dict[str, Any]], mapping: MappingConfig | None = None, scenario: str | None = None) -> SyncReport:
    cfg = mapping or load_mapping(DEFAULT_MAPPING)
    scenario_name = scenario or cfg.scenario
    accepted: list[NormalizedRow] = []
    rejected = []
    duplicates: list[DuplicateRow] = []
    upserts: list[AirtableUpsertOperation] = []
    audit: list[SyncAuditEvent] = []
    seen: set[str] = set()
    merge_targets = cfg.merge_key_fields or [field.target_field for field in cfg.fields if field.merge_key]

    for idx, row in enumerate(rows, start=1):
        fields: dict[str, Any] = {}
        failed = False
        for field in cfg.fields:
            raw = row.get(field.source_field, None)
            empty = raw is None or norm_text(raw) == ""
            if empty and field.default is not None:
                raw = field.default
                empty = False
            if empty and field.required:
                code = ReasonCode.MISSING_REQUIRED_FIELD if field.source_field in row else ReasonCode.MAPPING_FIELD_MISSING
                rejected.append(build_rejected(idx, scenario_name, code, row, field.source_field))
                audit.append(SyncAuditEvent(row_number=idx, scenario=scenario_name, decision="rejected", reason_code=code.value))
                failed = True
                break
            if empty and field.empty_policy == "drop":
                continue
            try:
                value = apply_transform(raw, field.transform)
            except ValueError as exc:
                code = ReasonCode(str(exc)) if str(exc) in ReasonCode._value2member_map_ else ReasonCode.TYPE_MISMATCH
                rejected.append(build_rejected(idx, scenario_name, code, row, field.source_field))
                audit.append(SyncAuditEvent(row_number=idx, scenario=scenario_name, decision="rejected", reason_code=code.value))
                failed = True
                break
            if field.transform == "email" and value and "@" not in str(value):
                rejected.append(build_rejected(idx, scenario_name, ReasonCode.INVALID_EMAIL, row, field.source_field))
                audit.append(SyncAuditEvent(row_number=idx, scenario=scenario_name, decision="rejected", reason_code=ReasonCode.INVALID_EMAIL.value))
                failed = True
                break
            fields[field.target_field] = value
        if failed:
            continue
        merge_key = make_merge_key(fields, merge_targets)
        if merge_key in seen:
            duplicates.append(DuplicateRow(row_number=idx, scenario=scenario_name, merge_key=merge_key, original=row))
            audit.append(SyncAuditEvent(row_number=idx, scenario=scenario_name, decision="duplicate", reason_code=ReasonCode.DUPLICATE_MERGE_KEY.value))
            continue
        seen.add(merge_key)
        normalized = NormalizedRow(row_number=idx, scenario=scenario_name, merge_key=merge_key, fields=fields)
        accepted.append(normalized)
        record_prefix = scenario_name.replace("_", "-")
        idempotency_key = make_idempotency_key(scenario_name, merge_key, fields)
        upserts.append(AirtableUpsertOperation(record_id=f"{record_prefix}:{merge_key}", merge_on_fields=merge_targets, idempotency_key=idempotency_key, fields=fields))
        audit.append(SyncAuditEvent(row_number=idx, scenario=scenario_name, decision="accepted"))

    counts = SyncSummaryCounts(accepted=len(accepted), rejected=len(rejected), duplicates=len(duplicates), upserts=len(upserts))
    return SyncReport(
        scenario=scenario_name,
        summary_counts=counts,
        accepted_rows=accepted,
        rejected_rows=rejected,
        duplicate_rows=duplicates,
        airtable_upserts=upserts,
        audit_log=audit,
        handoff_notes="Review rejected rows, then apply upserts only after Airtable access is approved.",
        risk_notes=["Fixture-safe preview only; no Google Sheets or Airtable network calls were made.", "Airtable performUpsert merge fields must be verified against the live base before use."],
    )


def sync_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compatibility wrapper preserving the original public behavior."""
    seen: set[str] = set()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    upserts: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        normalized = {
            "customer_name": norm_text(row.get("customer_name")),
            "email": norm_email(row.get("email")),
            "company": norm_text(row.get("company")),
            "status": norm_text(row.get("status")).lower() or "new",
            "estimated_value": norm_text(row.get("estimated_value")),
        }
        key = f"email:{normalized['email']}" if normalized["email"] else f"company-name:{normalized['company'].lower()}:{normalized['customer_name'].lower()}"
        if key in seen:
            duplicates.append(normalized | {"row_number": idx, "dedupe_key": key})
            audit.append({"row_number": idx, "decision": "duplicate", "live_services_used": False})
            continue
        seen.add(key)
        if not normalized["email"]:
            rejected.append(normalized | {"row_number": idx, "reason": "missing_required_field: email"})
            audit.append({"row_number": idx, "decision": "rejected", "live_services_used": False})
            continue
        accepted.append(normalized | {"row_number": idx})
        upserts.append({
            "system": "airtable",
            "operation": "upsert",
            "record_id": f"lead:{normalized['email']}",
            "fields": {
                "Name": normalized["customer_name"],
                "Email": normalized["email"],
                "Company": normalized["company"],
                "Status": normalized["status"],
                "Estimated Value": normalized["estimated_value"],
            },
        })
        audit.append({"row_number": idx, "decision": "accepted", "live_services_used": False})
    return {
        "accepted_rows": accepted,
        "rejected_rows": rejected,
        "duplicate_rows": duplicates,
        "airtable_upserts": upserts,
        "audit_log": audit,
        "handoff_notes": "Review rejected rows, then apply upserts only after Airtable access is approved.",
        "summary_counts": {"accepted": len(accepted), "rejected": len(rejected), "duplicates": len(duplicates), "upserts": len(upserts)},
        "fixture_safe": True,
        "live_services_used": False,
        "synthetic_data_only": True,
    }


def report_to_legacy_dict(report: SyncReport) -> dict[str, Any]:
    accepted = [{**row.fields, "row_number": row.row_number, "merge_key": row.merge_key} for row in report.accepted_rows]
    # compatibility aliases used by the original tests
    for row in accepted:
        if "Email" in row:
            row.setdefault("email", row["Email"])
            row.setdefault("status", str(row.get("Status", "")).lower())
    rejected = []
    for rejected_row in report.rejected_rows:
        item = dict(rejected_row.original)
        item.update({
            "row_number": rejected_row.row_number,
            "reason": rejected_row.reason,
            "reason_code": rejected_row.reason_code.value,
        })
        if "email" in item:
            item["email"] = norm_email(item.get("email"))
        rejected.append(item)
    duplicates = []
    for duplicate_row in report.duplicate_rows:
        item = dict(duplicate_row.original)
        item.update({
            "row_number": duplicate_row.row_number,
            "dedupe_key": duplicate_row.merge_key,
            "merge_key": duplicate_row.merge_key,
        })
        if "email" in item:
            item["email"] = norm_email(item.get("email"))
        duplicates.append(item)
    return {
        "accepted_rows": accepted,
        "rejected_rows": rejected,
        "duplicate_rows": duplicates,
        "airtable_upserts": [op.model_dump(mode="json") for op in report.airtable_upserts],
        "audit_log": [event.model_dump(mode="json") for event in report.audit_log],
        "handoff_notes": report.handoff_notes,
        "summary_counts": report.summary_counts.model_dump(),
        "fixture_safe": True,
        "live_services_used": False,
        "synthetic_data_only": True,
    }


def run_scenario(name: str) -> SyncReport:
    if name not in SCENARIOS:
        raise KeyError(f"unknown scenario: {name}")
    input_rel, mapping_rel = SCENARIOS[name]
    rows = load_rows(ROOT / input_rel)
    mapping = load_mapping(ROOT / mapping_rel)
    return sync_rows_with_mapping(rows, mapping, name)
