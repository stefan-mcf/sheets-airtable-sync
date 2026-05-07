from __future__ import annotations

from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel

from sheets_airtable_sync.backbone import get_health
from sheets_airtable_sync.config import load_mapping, load_rows
from sheets_airtable_sync.reports import render_report
from sheets_airtable_sync.sync import ROOT, list_scenarios, sync_rows_with_mapping

app = FastAPI(title="Sheets Airtable Sync", version="0.2.0", description="Fixture-safe local API for Sheets to Airtable sync previews.")


class SyncPreviewRequest(BaseModel):
    input_path: str
    mapping_path: str


class ReportRenderRequest(SyncPreviewRequest):
    format: Literal["json", "md", "html"] = "md"


class MappingValidateRequest(BaseModel):
    mapping_path: str


@app.get("/health")
def health() -> dict[str, Any]:
    return get_health()


@app.get("/examples")
def examples() -> dict[str, Any]:
    return {"examples": list_scenarios(), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}


@app.post("/sync/preview")
def sync_preview(request: SyncPreviewRequest) -> dict[str, Any]:
    report = sync_rows_with_mapping(load_rows(ROOT / request.input_path), load_mapping(ROOT / request.mapping_path))
    return report.model_dump(mode="json")


@app.post("/reports/render")
def reports_render(request: ReportRenderRequest) -> dict[str, Any]:
    report = sync_rows_with_mapping(load_rows(ROOT / request.input_path), load_mapping(ROOT / request.mapping_path))
    return {"format": request.format, "content": render_report(report, request.format), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}


@app.post("/mappings/validate")
def mappings_validate(request: MappingValidateRequest) -> dict[str, Any]:
    mapping = load_mapping(ROOT / request.mapping_path)
    return {"ok": True, "mapping": mapping.model_dump(mode="json"), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}
