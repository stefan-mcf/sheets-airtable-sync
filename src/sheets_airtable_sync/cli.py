from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from sheets_airtable_sync.backbone import get_health
from sheets_airtable_sync.config import load_mapping, load_rows
from sheets_airtable_sync.examples import validate_examples as validate_all_examples
from sheets_airtable_sync.reports import render_report, write_report
from sheets_airtable_sync.sync import list_scenarios, run_scenario, sync_rows_with_mapping

app = typer.Typer(help="Fixture-safe Sheets to Airtable sync proof CLI.", no_args_is_help=True)


def _print_json(payload: object) -> None:
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def health(json_output: Annotated[bool, typer.Option("--json")] = False) -> None:
    payload = get_health()
    if json_output:
        _print_json(payload)
    else:
        typer.echo("sheets-airtable-sync OK fixture_safe=true live_services_used=false")


@app.command()
def examples() -> None:
    _print_json(list_scenarios())


@app.command()
def validate(input_path: Path, mapping: Annotated[Path, typer.Option("--mapping")]) -> None:
    report = sync_rows_with_mapping(load_rows(input_path), load_mapping(mapping))
    _print_json({"ok": report.summary_counts.rejected == 0, "summary_counts": report.summary_counts.model_dump(), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True})


@app.command("plan-upserts")
def plan_upserts(input_path: Path, mapping: Annotated[Path, typer.Option("--mapping")]) -> None:
    report = sync_rows_with_mapping(load_rows(input_path), load_mapping(mapping))
    _print_json({"airtable_upserts": [op.model_dump(mode="json") for op in report.airtable_upserts], "summary_counts": report.summary_counts.model_dump(), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True})


@app.command()
def report(
    input_path: Path,
    mapping: Annotated[Path, typer.Option("--mapping")],
    format: str = "md",
    output: Path | None = None,
) -> None:
    if format not in {"json", "md", "html"}:
        raise typer.BadParameter("format must be json, md, or html")
    sync_report = sync_rows_with_mapping(load_rows(input_path), load_mapping(mapping))
    if output:
        write_report(sync_report, output, format)  # type: ignore[arg-type]
        _print_json({"written": str(output), "fixture_safe": True, "live_services_used": False, "synthetic_data_only": True})
    else:
        typer.echo(render_report(sync_report, format))  # type: ignore[arg-type]


@app.command("validate-examples")
def validate_examples() -> None:
    _print_json(validate_all_examples())


@app.command("run-scenario")
def run_scenario_command(name: str, format: str = "json") -> None:
    if format not in {"json", "md", "html"}:
        raise typer.BadParameter("format must be json, md, or html")
    typer.echo(render_report(run_scenario(name), format))  # type: ignore[arg-type]


if __name__ == "__main__":
    app()
