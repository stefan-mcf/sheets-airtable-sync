from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageStat, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "docs" / "screenshots"

WIDTH = 1400
HEIGHT = 800
BG = "#0b1120"
PANEL = "#111827"
HEADER = "#182235"
BORDER = "#334155"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
ACCENT = "#60a5fa"
SUCCESS = "#4ade80"
ERROR = "#f87171"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        (
            "/System/Library/Fonts/Menlo.ttc",
            1 if bold else 0,
        ),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            0,
        ),
        (
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
            0,
        ),
    ]
    for candidate, index in candidates:
        try:
            return ImageFont.truetype(candidate, size=size, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = font(34, bold=True)
SUBTITLE_FONT = font(18)
PANEL_TITLE_FONT = font(18, bold=True)
BODY_FONT = font(16)
CODE_FONT = font(15)
FOOTER_FONT = font(15)


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text())


def public_text(value: str) -> str:
    cleaned = value.replace(str(ROOT), ".").replace(str(Path.home()), "<home>")
    return re.sub(r"\s+in\s+\d+(?:\.\d+)?s\b", "", cleaned)


def display_command(command: list[str]) -> str:
    rendered = ["python" if part == sys.executable else public_text(part) for part in command]
    return shlex.join(rendered)


def run_cmd(command: list[str], *, timeout: int = 90, max_lines: int = 5) -> list[str]:
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
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out: {display_command(command)}") from exc
    output = public_text(result.stdout.strip())
    if result.returncode != 0:
        raise RuntimeError(
            f"command returned {result.returncode}: {display_command(command)}\n{output}"
        )
    lines = output.splitlines()[-max_lines:] if output else ["completed with no output"]
    return [f"$ {display_command(command)}", "PASS", *lines]


def run_json_cmd(
    command: list[str],
    fields: list[tuple[str, ...]],
    *,
    timeout: int = 90,
) -> list[str]:
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
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out: {display_command(command)}") from exc
    output = public_text(result.stdout.strip())
    if result.returncode != 0:
        raise RuntimeError(
            f"command returned {result.returncode}: {display_command(command)}\n{output}"
        )
    try:
        payload = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not return JSON: {display_command(command)}") from exc
    lines = [f"$ {display_command(command)}", "PASS"]
    for path in fields:
        value: Any = payload
        for part in path:
            value = value[part]
        rendered = (
            json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
        )
        lines.append(
            f"{'.'.join(path)}={rendered.lower() if isinstance(value, bool) else rendered}"
        )
    return lines


def generate_example_outputs() -> None:
    run_cmd([sys.executable, "scripts/verify_examples.py"], timeout=90, max_lines=2)


def wrap_lines(lines: list[str], width: int) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        if not line:
            wrapped.append("")
            continue
        wrapped.extend(
            textwrap.wrap(
                public_text(line),
                width=width,
                replace_whitespace=False,
                drop_whitespace=False,
            )
            or [line]
        )
    return wrapped


def draw_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    *,
    accent: str = ACCENT,
    code: bool = False,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=20, fill=PANEL, outline=BORDER, width=2)
    draw.rectangle((x1, y1 + 20, x1 + 5, y2 - 20), fill=accent)
    draw.text((x1 + 26, y1 + 20), title, font=PANEL_TITLE_FONT, fill=accent)
    selected_font = CODE_FONT if code else BODY_FONT
    max_chars = max(34, (x2 - x1 - 68) // (9 if code else 10))
    y = y1 + 58
    for line in wrap_lines(lines, max_chars):
        if y > y2 - 34:
            break
        fill = TEXT
        if line == "PASS" or line.startswith(("fixture_safe=true", "provider_writes=false")):
            fill = SUCCESS
        elif line.startswith(("rejected", "blocked", "invalid")):
            fill = ERROR
        elif line.startswith(("$", "GET ", "POST ")):
            fill = ACCENT
        draw.text((x1 + 26, y), line, font=selected_font, fill=fill)
        y += 24 if code else 27


def validate_public_copy(copy: str) -> None:
    forbidden = ("pro" + "of", "evi" + "dence", "walk" + "through", "tuto" + "rial")
    lowered = copy.lower()
    matches = [term for term in forbidden if term in lowered]
    if matches:
        raise RuntimeError(f"public copy contains retired terminology: {matches}")
    local_prefixes = ("/" + "Users/", "/" + "home/")
    if any(prefix in copy for prefix in local_prefixes) or "command_exit_code" in copy:
        raise RuntimeError("public copy contains a local path or command error marker")


def render(
    path: Path,
    title: str,
    subtitle: str,
    panels: list[dict[str, Any]],
    *,
    footer: str = "Local inputs | No provider writes | Synthetic records",
) -> None:
    public_copy = json.dumps(
        {
            "title": title,
            "subtitle": subtitle,
            "footer": footer,
            "panels": [
                {"title": str(panel["title"]), "lines": list(panel["lines"])} for panel in panels
            ],
        },
        sort_keys=True,
    )
    public_copy = public_text(public_copy)
    validate_public_copy(public_copy)

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((32, 28, 1368, 122), radius=24, fill=HEADER, outline=BORDER, width=2)
    draw.text((60, 50), title, font=TITLE_FONT, fill=TEXT)
    draw.text((60, 94), subtitle, font=SUBTITLE_FONT, fill=MUTED)
    for panel in panels:
        draw_panel(
            draw,
            panel["box"],
            str(panel["title"]),
            list(panel["lines"]),
            accent=str(panel.get("accent", ACCENT)),
            code=bool(panel.get("code", False)),
        )
    draw.rounded_rectangle((32, 730, 1368, 772), radius=16, fill=HEADER, outline=BORDER, width=1)
    draw.text((56, 741), footer, font=FOOTER_FONT, fill=MUTED)

    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("PortfolioCopy", public_copy)
    metadata.add_text("ValidationStatus", "passed")
    image.save(path, pnginfo=metadata, optimize=True)

    stat = ImageStat.Stat(image)
    if path.stat().st_size < 30_000 or max(stat.stddev) < 18:
        raise RuntimeError(
            f"image may be unreadable: {path.name} size={path.stat().st_size} stddev={stat.stddev}"
        )


def render_system_flow() -> None:
    crm = read_json("examples/output/crm-leads-sync-report.json")
    dirty = read_json("examples/output/dirty-rows-sync-report.json")
    render(
        OUT / "01-system-flow.png",
        "Sheets to Airtable system flow",
        "Rows are validated, normalised, reconciled, and prepared before any provider write.",
        [
            {
                "box": (52, 154, 452, 670),
                "title": "Source rows",
                "lines": [
                    "CRM lead export",
                    "Shopify order export",
                    "Project tracker",
                    "Google Form responses",
                    "Notion-style records",
                    "Mapping and merge-key config",
                ],
            },
            {
                "box": (500, 154, 900, 670),
                "title": "Reconciliation",
                "lines": [
                    "Validate required fields",
                    "Reject unsafe formulas",
                    "Normalise typed values",
                    "Detect duplicate merge keys",
                    "Create idempotency keys",
                    "Prepare Airtable operations",
                ],
            },
            {
                "box": (948, 154, 1348, 670),
                "title": "Prepared result",
                "lines": [
                    f"crm accepted={crm['summary_counts']['accepted']}",
                    f"crm rejected={crm['summary_counts']['rejected']}",
                    f"crm upserts={crm['summary_counts']['upserts']}",
                    f"dirty duplicates={dirty['summary_counts']['duplicates']}",
                    "JSON, Markdown, and HTML reports",
                    "Provider write remains gated",
                ],
                "accent": SUCCESS,
            },
        ],
    )


def render_interface_surface() -> None:
    cli_lines = [
        *run_json_cmd(
            [sys.executable, "-m", "sheets_airtable_sync.cli", "health", "--json"],
            [
                ("package",),
                ("fixture_safe",),
                ("synthetic_data_only",),
                ("live_services_used",),
            ],
            timeout=30,
        ),
        "",
        *run_json_cmd(
            [
                sys.executable,
                "-m",
                "sheets_airtable_sync.cli",
                "validate",
                "examples/input/dirty-rows.json",
                "--mapping",
                "configs/mappings/leads-to-airtable.json",
            ],
            [
                ("summary_counts", "accepted"),
                ("summary_counts", "duplicates"),
                ("summary_counts", "rejected"),
                ("summary_counts", "upserts"),
            ],
            timeout=30,
        ),
    ]
    render(
        OUT / "02-interface-surface.png",
        "Operator interfaces",
        "CLI, API, MCP, and shell controls expose one reconciliation contract.",
        [
            {
                "box": (52, 154, 674, 670),
                "title": "CLI readback",
                "lines": cli_lines,
                "code": True,
            },
            {
                "box": (726, 154, 1348, 670),
                "title": "API and adapters",
                "lines": [
                    "GET /health",
                    "GET /examples",
                    "POST /sync/preview",
                    "POST /reports/render",
                    "POST /mappings/validate",
                    "",
                    "MCP: list scenarios",
                    "MCP: validate rows",
                    "MCP: plan Airtable upserts",
                    "MCP: render sync report",
                    "",
                    "Executor: health, validate, preview, report, verify",
                ],
                "code": True,
            },
        ],
    )


def render_core_processing() -> None:
    scenarios = [
        "crm-leads",
        "shopify-orders",
        "project-tracker",
        "google-form-responses",
        "notion-database-rows",
        "dirty-rows",
    ]
    counts = []
    for scenario in scenarios:
        summary = read_json(f"examples/output/{scenario}-sync-report.json")["summary_counts"]
        counts.append(
            f"{scenario}: ok={summary['accepted']} reject={summary['rejected']} "
            f"dupe={summary['duplicates']} upsert={summary['upserts']}"
        )
    upserts = read_json("examples/output/crm-leads-sync-report.json")["airtable_upserts"]
    render(
        OUT / "03-core-processing.png",
        "Core reconciliation",
        "Six committed scenarios exercise typed cleanup, duplicate control, and idempotent planning.",
        [
            {
                "box": (52, 154, 674, 670),
                "title": "Scenario counts",
                "lines": counts,
                "code": True,
            },
            {
                "box": (726, 154, 1348, 670),
                "title": "Airtable operation readback",
                "lines": [
                    f"operation={upserts[0]['operation']}",
                    f"record_id={upserts[0]['record_id']}",
                    f"merge_on_fields={upserts[0]['merge_on_fields']}",
                    f"idempotency_key={upserts[0]['idempotency_key']}",
                    f"fields={json.dumps(upserts[0]['fields'], sort_keys=True)}",
                    "",
                    "Prepared locally. Not submitted.",
                ],
                "code": True,
                "accent": SUCCESS,
            },
        ],
    )


def render_guardrail_path() -> None:
    crm = read_json("examples/output/crm-leads-sync-report.json")
    dirty = read_json("examples/output/dirty-rows-sync-report.json")
    rejected = crm["rejected_rows"] + dirty["rejected_rows"]
    duplicate = dirty["duplicate_rows"][0]
    flattened: list[str] = []
    for item in rejected:
        flattened.extend(
            [
                f"row={item['row_number']} reason={item['reason_code']}",
                f"action={item['suggested_remediation']}",
                "",
            ]
        )
    render(
        OUT / "04-guardrail-path.png",
        "Rejected-row and duplicate controls",
        "Unsafe or ambiguous rows stop with reason codes and operator-ready remediation.",
        [
            {
                "box": (52, 154, 674, 670),
                "title": "Rejected rows",
                "lines": flattened,
                "code": True,
                "accent": ERROR,
            },
            {
                "box": (726, 154, 1348, 670),
                "title": "Duplicate readback",
                "lines": [
                    f"scenario={duplicate['scenario']}",
                    f"row_number={duplicate['row_number']}",
                    f"merge_key={duplicate['merge_key']}",
                    f"reason_code={duplicate['reason_code']}",
                    f"original.company={duplicate['original']['company']}",
                    f"original.status={duplicate['original']['status']}",
                    "",
                    "No destination operation prepared for this row.",
                ],
                "code": True,
                "accent": ERROR,
            },
        ],
    )


def render_output_readback() -> None:
    report = read_json("examples/output/crm-leads-sync-report.json")
    first = report["accepted_rows"][0]
    make = read_json("templates/make/airtable-upsert-scenario.json")
    zapier = read_json("templates/zapier/sheets-to-airtable-zap.json")
    n8n = read_json("templates/n8n/sheets-airtable-sync.workflow.json")
    apps_script = (ROOT / "templates/gas/sheets-cleanup.gs").read_text()
    render(
        OUT / "05-output-readback.png",
        "Output and implementation handoff",
        "Normalised records, audit history, and provider blueprints stay inspectable before activation.",
        [
            {
                "box": (52, 154, 674, 670),
                "title": "Normalised record",
                "lines": [
                    f"scenario={first['scenario']}",
                    f"row_number={first['row_number']}",
                    f"merge_key={first['merge_key']}",
                    f"normalised={json.dumps(first['fields'], sort_keys=True)}",
                    "",
                    f"audit_events={len(report['audit_log'])}",
                    f"prepared_upserts={report['summary_counts']['upserts']}",
                ],
                "code": True,
                "accent": SUCCESS,
            },
            {
                "box": (726, 154, 1348, 670),
                "title": "Provider blueprints",
                "lines": [
                    f"n8n: {len(n8n['nodes'])} nodes; {len(n8n['connections'])} connection groups",
                    f"Make: {len(make['modules'])} configured modules",
                    f"Zapier: trigger plus {len(zapier['steps'])} configured steps",
                    "Apps Script: normalizeRowsFixtureOnly()"
                    if "normalizeRowsFixtureOnly" in apps_script
                    else "Apps Script: local cleanup function",
                    "",
                    "Credentials are omitted.",
                    "Provider activation requires separate approval.",
                ],
            },
        ],
    )


def render_validation_scope() -> None:
    render(
        OUT / "06-validation-scope.png",
        "Validation and operating scope",
        "Local checks are running before the final validation readback is written.",
        [
            {
                "box": (52, 154, 820, 670),
                "title": "Validation in progress",
                "lines": ["The final image replaces this temporary render."],
            },
            {
                "box": (872, 154, 1348, 670),
                "title": "Scope and image checks",
                "lines": ["Image sequence: 6 current files", "Dimensions: 1400 x 800"],
            },
        ],
    )
    validation_lines: list[str] = []
    commands = [
        ("Tests", [sys.executable, "-m", "pytest", "-q", "--disable-warnings"], 180),
        ("Lint", [sys.executable, "-m", "ruff", "check", "."], 90),
        ("Types", [sys.executable, "-m", "mypy", "src"], 120),
    ]
    for label, command, timeout in commands:
        summary = run_cmd(command, timeout=timeout, max_lines=1)[-1]
        validation_lines.append(f"{label}: {summary}")
    scenario_summary = run_json_cmd(
        [sys.executable, "scripts/verify_examples.py"],
        [("scenario_count",)],
        timeout=90,
    )[-1]
    validation_lines.append(f"Scenarios: {scenario_summary}")
    verifier_output = run_cmd(["./executor.sh", "verify"], timeout=90, max_lines=1)[-1]
    verifier_status = json.loads(verifier_output)
    validation_lines.append(f"Full verifier: verified={str(verifier_status['verified']).lower()}")
    render(
        OUT / "06-validation-scope.png",
        "Validation and operating scope",
        "Automated checks pass locally while all provider writes remain disabled.",
        [
            {
                "box": (52, 154, 820, 670),
                "title": "Core validation readback",
                "lines": validation_lines,
                "code": True,
                "accent": SUCCESS,
            },
            {
                "box": (872, 154, 1348, 670),
                "title": "Scope and image checks",
                "lines": [
                    "Image sequence: 6 current files",
                    "Dimensions: 1400 x 800",
                    "Public copy scanner enabled",
                    "",
                    "Synthetic fixtures only",
                    "Empty credential placeholders",
                    "No customer records",
                    "No network sync calls",
                    "No live Airtable writes",
                    "No live Google Sheets reads",
                    "Sandbox approval required for activation",
                ],
            },
        ],
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    generate_example_outputs()
    render_system_flow()
    render_interface_surface()
    render_core_processing()
    render_guardrail_path()
    render_output_readback()
    render_validation_scope()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
