from __future__ import annotations

from typing import Any, Literal, cast

from sheets_airtable_sync.backbone import get_health
from sheets_airtable_sync.config import load_mapping, load_rows
from sheets_airtable_sync.reports import render_report
from sheets_airtable_sync.sync import ROOT, list_scenarios, run_scenario, sync_rows_with_mapping


def get_sheets_airtable_health() -> dict[str, Any]:
    return get_health()


def list_sheets_airtable_scenarios() -> list[dict[str, str]]:
    return list_scenarios()


def validate_sheets_airtable_rows(input_path: str, mapping_path: str) -> dict[str, Any]:
    report = sync_rows_with_mapping(load_rows(ROOT / input_path), load_mapping(ROOT / mapping_path))
    return {"ok": report.summary_counts.rejected == 0, "summary_counts": report.summary_counts.model_dump(), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}


def plan_airtable_upserts(input_path: str, mapping_path: str) -> dict[str, Any]:
    report = sync_rows_with_mapping(load_rows(ROOT / input_path), load_mapping(ROOT / mapping_path))
    return {"airtable_upserts": [op.model_dump(mode="json") for op in report.airtable_upserts], "summary_counts": report.summary_counts.model_dump(), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}


def render_sync_report(scenario: str, format: str = "md") -> dict[str, Any]:
    if format not in {"json", "md", "html"}:
        raise ValueError("format must be json, md, or html")
    fmt = cast(Literal["json", "md", "html"], format)
    return {"content": render_report(run_scenario(scenario), fmt), "format": fmt, "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True}


def build_mcp_server() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception:
        return None
    mcp = FastMCP("sheets-airtable-sync")
    mcp.tool()(get_sheets_airtable_health)
    mcp.tool()(list_sheets_airtable_scenarios)
    mcp.tool()(validate_sheets_airtable_rows)
    mcp.tool()(plan_airtable_upserts)
    mcp.tool()(render_sync_report)
    return mcp


mcp = build_mcp_server()
