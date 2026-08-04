from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
issues: list[str] = []
retired_terms = ("pro" + "of", "evi" + "dence", "walk" + "through", "tuto" + "rial")

banned_patterns = [
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
    re.compile(r"PRIVATE KEY"),
    re.compile(r"api[_-]?key\s*[:=]\s*[A-Za-z0-9]"),
]

for rel in tracked:
    path = ROOT / rel
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    if rel != "scripts/public_readiness_check.py":
        for pattern in banned_patterns:
            if pattern.search(text):
                issues.append(f"{rel}: banned pattern {pattern.pattern}")
    public_copy = rel.endswith(".md") or rel in {
        "CONCEPT_SCOPE.md",
        "PLAN.md",
        "repo-metadata.json",
        "scripts/render_portfolio_images.py",
    }
    if public_copy:
        lowered = text.lower()
        for term in retired_terms:
            if term in lowered:
                issues.append(f"{rel}: retired public terminology {term}")
        if "—" in text or "–" in text:
            issues.append(f"{rel}: non-standard dash in public copy")

for rel in tracked:
    lowered_rel = rel.lower()
    for term in retired_terms:
        if term in lowered_rel:
            issues.append(f"{rel}: retired terminology in public path")

expected_images = {
    f"docs/screenshots/{index:02d}-{name}.png"
    for index, name in enumerate(
        [
            "system-flow",
            "interface-surface",
            "core-processing",
            "guardrail-path",
            "output-readback",
            "validation-scope",
        ],
        start=1,
    )
}
actual_images = {
    rel for rel in tracked if rel.startswith("docs/screenshots/") and rel.endswith(".png")
}
if actual_images != expected_images:
    issues.append("docs/screenshots: expected the standard six-image sequence")

report = {"ok": not issues, "issues": issues}
print(json.dumps(report, indent=2))
if issues:
    raise SystemExit(1)
