from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Literal

from sheets_airtable_sync.models import SyncReport


def report_to_json(report: SyncReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"


def report_to_markdown(report: SyncReport) -> str:
    counts = report.summary_counts
    lines = [
        f"# Sync Report — {report.scenario}", "",
        "Fixture-safe local proof. No live Google Sheets or Airtable calls were made.", "",
        "## Summary", "",
        f"- Accepted rows: {counts.accepted}", f"- Rejected rows: {counts.rejected}",
        f"- Duplicate rows: {counts.duplicates}", f"- Airtable upsert previews: {counts.upserts}", "",
        "## Accepted sample", "",
    ]
    for row in report.accepted_rows[:5]:
        lines.append(f"- Row {row.row_number}: merge key `{row.merge_key}` -> {row.fields}")
    if not report.accepted_rows:
        lines.append("- None")
    lines += ["", "## Rejected rows", ""]
    if report.rejected_rows:
        lines += ["| Row | Reason code | Remediation |", "|---:|---|---|"]
        for rejected_row in report.rejected_rows:
            lines.append(
                f"| {rejected_row.row_number} | `{rejected_row.reason_code.value}` | "
                f"{rejected_row.suggested_remediation} |"
            )
    else:
        lines.append("- None")
    lines += ["", "## Duplicate keys", ""]
    if report.duplicate_rows:
        for duplicate_row in report.duplicate_rows:
            lines.append(f"- Row {duplicate_row.row_number}: `{duplicate_row.merge_key}`")
    else:
        lines.append("- None")
    lines += ["", "## Airtable upsert preview", ""]
    for op in report.airtable_upserts[:10]:
        lines.append(f"- `{op.record_id}` merge on {', '.join(op.merge_on_fields)} idempotency `{op.idempotency_key}`")
    lines += ["", "## Risk notes", ""]
    for note in report.risk_notes:
        lines.append(f"- {note}")
    lines += ["", "## Live-gate next steps", "", "1. Confirm target base/table schema.", "2. Create scoped Airtable PAT/OAuth and Google auth outside this repo.", "3. Run sandbox with explicit live approval only.", ""]
    return "\n".join(lines)


def report_to_html(report: SyncReport) -> str:
    body = html.escape(report_to_markdown(report)).replace("\n", "<br>\n")
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(report.scenario)} Sync Report</title><style>body{{font-family:ui-monospace,monospace;max-width:980px;margin:2rem auto;line-height:1.5}}code{{background:#eef;padding:2px 4px}}</style></head><body>{body}</body></html>\n"


def render_report(report: SyncReport, fmt: Literal["json", "md", "html"] = "md") -> str:
    if fmt == "json":
        return report_to_json(report)
    if fmt == "html":
        return report_to_html(report)
    return report_to_markdown(report)


def write_report(report: SyncReport, output: str | Path, fmt: Literal["json", "md", "html"] = "md") -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(report, fmt), encoding="utf-8")
    return path
