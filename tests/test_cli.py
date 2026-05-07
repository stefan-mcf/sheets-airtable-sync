import json

from typer.testing import CliRunner

from sheets_airtable_sync.cli import app

runner = CliRunner()


def test_cli_health_json() -> None:
    result = runner.invoke(app, ["health", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["fixture_safe"] is True


def test_cli_validate_and_plan() -> None:
    args = ["examples/input/crm-leads.json", "--mapping", "configs/mappings/leads-to-airtable.json"]
    assert runner.invoke(app, ["validate", *args]).exit_code == 0
    preview = runner.invoke(app, ["plan-upserts", *args])
    assert preview.exit_code == 0
    assert json.loads(preview.stdout)["airtable_upserts"]


def test_cli_report_to_file(tmp_path) -> None:
    out = tmp_path / "report.md"
    result = runner.invoke(app, ["report", "examples/input/crm-leads.json", "--mapping", "configs/mappings/leads-to-airtable.json", "--format", "md", "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
