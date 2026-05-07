from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sheets_airtable_sync.examples import validate_examples
from sheets_airtable_sync.reports import write_report
from sheets_airtable_sync.sync import ROOT, list_scenarios, run_scenario


def main() -> int:
    result = validate_examples()
    output_dir = ROOT / "examples" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in list_scenarios():
        report = run_scenario(item["name"])
        stem = item["name"]
        (output_dir / f"{stem}-sync-report.json").write_text(json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_report(report, output_dir / f"{stem}-report.md", "md")
        write_report(report, output_dir / f"{stem}-report.html", "html")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
