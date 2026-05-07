import json
import subprocess


def test_executor_health() -> None:
    out = subprocess.check_output(["./executor.sh", "health"], text=True)
    assert json.loads(out)["fixture_safe"] is True


def test_executor_preview() -> None:
    out = subprocess.check_output(["./executor.sh", "preview", "crm-leads"], text=True)
    assert json.loads(out)["airtable_upserts"]
