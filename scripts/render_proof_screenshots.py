from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "docs" / "screenshots"
SIZE = (1600, 1000)
BG = "#0f172a"
CARD = "#111827"
CARD_2 = "#1e293b"
TEXT = "#f8fafc"
MUTED = "#cbd5e1"
FAINT = "#94a3b8"
CYAN = "#38bdf8"
GREEN = "#22c55e"
AMBER = "#f59e0b"
PINK = "#fb7185"
PURPLE = "#a78bfa"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size, index=1 if bold and candidate.endswith(".ttc") else 0)
        except Exception:
            pass
    return ImageFont.load_default()


TITLE = font(44, bold=True)
SUBTITLE = font(24)
BODY = font(21)
SMALL = font(18)
MONO = font(16)
MONO_SMALL = font(14)


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text())


def run_cmd(command: list[str], timeout: int = 90) -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "$ " + " ".join(command) + "\nTIMEOUT"
    output = result.stdout.strip()
    if len(output) > 900:
        output = output[:900].rstrip() + "\n..."
    status = "PASS" if result.returncode == 0 else f"FAIL exit={result.returncode}"
    return "$ " + " ".join(command) + f"\n{status}\n" + output


def canvas(title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", SIZE, BG)
    d = ImageDraw.Draw(img)
    d.rectangle((40, 40, SIZE[0] - 40, SIZE[1] - 40), outline=CYAN, width=4)
    d.text((80, 76), "Sheets Airtable Sync", fill="#93c5fd", font=font(35, bold=True))
    d.text((80, 132), title, fill=TEXT, font=TITLE)
    d.text((80, 205), "Fixture-safe proof from committed JSON, templates, CLI/API commands, and local gates", fill=MUTED, font=SUBTITLE)
    d.text((80, 238), "synthetic_data_only=true  live_services_used=false  provider/network sync calls disabled", fill=FAINT, font=SMALL)
    return img, d


def wrap(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for raw in str(text).splitlines() or [""]:
        if not raw:
            lines.append("")
        else:
            lines.extend(textwrap.wrap(raw, width=width, replace_whitespace=False, drop_whitespace=False) or [raw])
    return lines


def card(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    heading: str,
    lines: list[str],
    *,
    accent: str = CYAN,
    mono: bool = False,
) -> None:
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=18, fill=CARD, outline=accent, width=3)
    heading_font = font(21, bold=True)
    heading_chars = max(20, int((x2 - x1 - 44) / 11))
    y = y1 + 18
    for heading_part in wrap(heading, heading_chars)[:2]:
        d.text((x1 + 22, y), heading_part, fill=accent, font=heading_font)
        y += 25
    y += 8
    fnt = MONO if mono else BODY
    max_chars = max(24, int((x2 - x1 - 54) / (11.8 if mono else 11.5)))
    for line in lines:
        for part in wrap(line, max_chars):
            if y + 24 > y2 - 14:
                d.text((x1 + 22, y), "…", fill=FAINT, font=fnt)
                return
            d.text((x1 + 22, y), part, fill=TEXT if not part.startswith(("$", "PASS", "{")) else MUTED, font=fnt)
            y += 24 if mono else 30


def table_card(d: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], heading: str, rows: list[list[str]], widths: list[int]) -> None:
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=18, fill=CARD, outline=GREEN, width=3)
    d.text((x1 + 22, y1 + 18), heading, fill=GREEN, font=font(24, bold=True))
    y = y1 + 64
    for i, row in enumerate(rows):
        x = x1 + 22
        fill = MUTED if i == 0 else TEXT
        for col, width in zip(row, widths):
            d.text((x, y), col[: int(width / 10)], fill=fill, font=MONO)
            x += width
        y += 30
        if y > y2 - 30 and i < len(rows) - 1:
            d.text((x1 + 22, y), "…", fill=FAINT, font=MONO)
            break


def footer(d: ImageDraw.ImageDraw, text: str) -> None:
    d.text((80, 910), text, fill=FAINT, font=SMALL)


def render_flow() -> None:
    crm = read_json("examples/output/crm-leads-sync-report.json")
    dirty = read_json("examples/output/dirty-rows-sync-report.json")
    img, d = canvas("01 — Flow overview")
    rows = [
        ["stage", "evidence from artifacts"],
        ["input", "crm-leads: 4 rows; dirty-rows: 3 rows"],
        ["validate", "unsafe formulas + invalid/missing emails rejected"],
        ["dedupe", f"dirty-rows duplicate merge key: {dirty['duplicate_rows'][0]['merge_key']}"],
        ["preview", f"crm-leads: {crm['summary_counts']['upserts']} Airtable-shaped upserts"],
    ]
    table_card(d, (80, 295, 1500, 520), "Pipeline evidence", rows, [190, 1060])
    card(d, (80, 555, 760, 865), "Actual accepted row", [
        "source row_number=2 / scenario=crm-leads",
        "Name=Omar Patel",
        "Email=omar@example.com",
        "Estimated Value=$8,100 -> 8100.00",
        "Status=Active Customer -> active",
    ], accent=GREEN)
    card(d, (820, 555, 1500, 865), "Actual rejected row", [
        "source row_number=4 / scenario=crm-leads",
        "email=not-an-email",
        "reason_code=invalid_email",
        "remediation=Correct email, then retry row.",
    ], accent=PINK)
    footer(d, "This is not a live-service screenshot; it proves deterministic local transformation and safety behavior from committed fixtures.")
    img.save(OUT / "01-flow-overview.png")


def render_cli() -> None:
    img, d = canvas("02 — CLI commands with captured output")
    outputs = [
        run_cmd([sys.executable, "-m", "sheets_airtable_sync.cli", "health", "--json"], 30),
        run_cmd([sys.executable, "-m", "sheets_airtable_sync.cli", "validate", "examples/input/dirty-rows.json", "--mapping", "configs/mappings/leads-to-airtable.json"], 30),
        run_cmd([sys.executable, "-m", "sheets_airtable_sync.cli", "plan-upserts", "examples/input/crm-leads.json", "--mapping", "configs/mappings/leads-to-airtable.json"], 30),
    ]
    card(d, (80, 295, 1500, 865), "Captured local CLI proof", "\n\n".join(outputs).splitlines(), accent=CYAN, mono=True)
    footer(d, "Renderer executes these commands locally when screenshots are regenerated; failures appear in the panel.")
    img.save(OUT / "02-cli-proof.png")


def render_api() -> None:
    health = read_json("examples/api-responses/health.json")
    response = read_json("examples/api-responses/sync-preview-response.json")
    img, d = canvas("03 — API surface and response contract")
    card(d, (80, 295, 760, 865), "OpenAPI endpoints", [
        "GET /health -> fixture-safe service status",
        "GET /examples -> available fixture scenarios",
        "POST /sync/preview -> validation + upsert preview",
        "POST /reports/render -> markdown/html/json report rendering",
        "No credentials required for local proof paths.",
    ], accent=PURPLE)
    card(d, (820, 295, 1500, 865), "Sample response facts", [
        json.dumps({
            "health": health,
            "scenario": response["scenario"],
            "summary_counts": response["summary_counts"],
            "fixture_safe": response["fixture_safe"],
            "live_services_used": response["live_services_used"],
        }, indent=2),
    ], accent=GREEN, mono=True)
    footer(d, "The API proof is local/fixture-safe; live Airtable/Sheets auth remains behind the documented integration gate.")
    img.save(OUT / "03-openapi-endpoints.png")


def render_sync_preview() -> None:
    scenarios = ["crm-leads", "shopify-orders", "project-tracker", "google-form-responses", "notion-database-rows", "dirty-rows"]
    rows = [["scenario", "accepted", "rejected", "dupes", "upserts"]]
    for scenario in scenarios:
        report = read_json(f"examples/output/{scenario}-sync-report.json")
        counts = report["summary_counts"]
        rows.append([scenario, str(counts["accepted"]), str(counts["rejected"]), str(counts["duplicates"]), str(counts["upserts"])])
    img, d = canvas("04 — Sync preview by scenario")
    table_card(d, (80, 295, 1500, 570), "Generated summary_counts from committed outputs", rows, [390, 170, 170, 170, 170])
    report = read_json("examples/output/dirty-rows-sync-report.json")
    card(d, (80, 610, 1500, 865), "dirty-rows audit trail excerpt", [
        json.dumps(report["audit_log"], indent=2),
    ], accent=AMBER, mono=True)
    footer(d, "This panel now shows actual counts and decisions, not placeholder metric labels.")
    img.save(OUT / "04-sync-preview.png")


def render_upserts() -> None:
    report = read_json("examples/output/crm-leads-sync-report.json")
    upserts = report["airtable_upserts"]
    img, d = canvas("05 — Airtable-shaped upsert output")
    card(d, (80, 295, 760, 865), "Upsert #1", [json.dumps(upserts[0], indent=2)], accent=GREEN, mono=True)
    card(d, (820, 295, 1500, 865), "Upsert #2", [
        "operation=upsert",
        f"record_id={upserts[1]['record_id']}",
        f"merge_on_fields={upserts[1]['merge_on_fields']}",
        f"idempotency_key={upserts[1]['idempotency_key']}",
        "fields:",
        json.dumps(upserts[1]["fields"], indent=2),
    ], accent=CYAN, mono=True)
    footer(d, "Airtable-ready payloads are generated but not submitted; applying them requires live-integration approval.")
    img.save(OUT / "05-upsert-output.png")


def render_rejections() -> None:
    crm = read_json("examples/output/crm-leads-sync-report.json")
    dirty = read_json("examples/output/dirty-rows-sync-report.json")
    rejected = crm["rejected_rows"] + dirty["rejected_rows"]
    duplicate = dirty["duplicate_rows"][0]
    rows = [["row", "scenario", "reason_code", "remediation"]]
    for item in rejected:
        rows.append([
            str(item["row_number"]),
            item["scenario"],
            item["reason_code"],
            item["suggested_remediation"],
        ])
    img, d = canvas("06 — Dead-letter and duplicate handling")
    table_card(d, (80, 295, 1500, 570), "Rejected rows with reason taxonomy", rows, [90, 280, 300, 700])
    original = duplicate["original"]
    card(d, (80, 610, 1500, 865), "Duplicate evidence", [
        f"scenario={duplicate['scenario']}",
        f"row_number={duplicate['row_number']}",
        f"merge_key={duplicate['merge_key']}",
        f"reason_code={duplicate['reason_code']}",
        f"original.company={original['company']}",
        f"original.email={original['email']}",
        f"original.status={original['status']}",
    ], accent=AMBER, mono=True)
    footer(d, "The screenshot proves specific error branches: invalid email, unsafe formula, missing field, and duplicate merge key.")
    img.save(OUT / "06-rejected-rows.png")


def render_handoff() -> None:
    img, d = canvas("07 — Handoff templates")
    summaries = [
        ("Make template", "templates/make/airtable-upsert-scenario.json", [
            "input: sync preview JSON",
            "action: Airtable upsert shape",
            "merge field: Email",
            "safety: credentials omitted",
        ]),
        ("Zapier template", "templates/zapier/sheets-to-airtable-zap.json", [
            "trigger: new/updated row",
            "webhook: local preview API",
            "filter: only fixture-safe output",
            "safety: no live Zap connected",
        ]),
        ("n8n template", "templates/n8n/sheets-airtable-sync.workflow.json", [
            "nodes: schedule + HTTP request",
            "maps preview to Airtable-ready ops",
            "dead letters stay review-first",
            "safety: importable blueprint only",
        ]),
        ("Apps Script template", "templates/gas/sheets-cleanup.gs", [
            "normalizes exported sheet rows",
            "strips formulas before handoff",
            "flags missing required fields",
            "safety: sample script only",
        ]),
    ]
    positions = [(80, 295, 760, 560), (820, 295, 1500, 560), (80, 600, 760, 865), (820, 600, 1500, 865)]
    accents = [GREEN, AMBER, PURPLE, CYAN]
    for (name, rel, lines), xy, accent in zip(summaries, positions, accents):
        card(d, xy, name, [f"path={rel}", *lines], accent=accent, mono=True)
    footer(d, "Committed handoff artifacts only; no live Make, Zapier, n8n, or Apps Script accounts are connected.")
    img.save(OUT / "07-platform-handoff.png")


def render_quality() -> None:
    img, d = canvas("08 — Quality gates captured during render")
    gates = [
        run_cmd([sys.executable, "-m", "pytest", "-q"], 180),
        run_cmd([sys.executable, "-m", "ruff", "check", "."], 90),
        run_cmd([sys.executable, "-m", "mypy", "src"], 120),
        run_cmd([sys.executable, "scripts/verify_examples.py"], 60),
        run_cmd(["./executor.sh", "verify"], 90),
    ]
    card(d, (80, 295, 1500, 865), "Local gate output", "\n\n".join(gates).splitlines(), accent=GREEN, mono=True)
    footer(d, "This panel is regenerated from command output; it is still local proof, not a live-provider integration test.")
    img.save(OUT / "08-quality-gates.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    render_flow()
    render_cli()
    render_api()
    render_sync_preview()
    render_upserts()
    render_rejections()
    render_handoff()
    render_quality()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
