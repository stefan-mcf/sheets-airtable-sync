#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:-src}"
LIVE_ALLOWED="${SHEETS_AIRTABLE_SYNC_LIVE_SERVICES:-false}"
cmd="${1:-help}"; shift || true
scenario_to_paths() {
  case "$1" in
    dirty-rows) echo "examples/input/dirty-rows.json configs/mappings/leads-to-airtable.json";;
    crm-leads) echo "examples/input/crm-leads.json configs/mappings/leads-to-airtable.json";;
    shopify-orders) echo "examples/input/shopify-orders.json configs/mappings/shopify-orders-to-airtable.json";;
    project-tracker) echo "examples/input/project-tracker.json configs/mappings/project-tracker-to-airtable.json";;
    google-form-responses) echo "examples/input/google-form-responses.json configs/mappings/form-responses-to-airtable.json";;
    *) echo "unknown scenario: $1" >&2; return 2;;
  esac
}
refuse_live() {
  if [ "$LIVE_ALLOWED" = "true" ] && [ "${SHEETS_AIRTABLE_SYNC_EXPLICIT_LIVE_APPROVAL:-false}" != "true" ]; then
    echo '{"ok":false,"error":"live mode requires SHEETS_AIRTABLE_SYNC_EXPLICIT_LIVE_APPROVAL=true","live_services_used":false}'
    exit 3
  fi
}
refuse_live
case "$cmd" in
  health) python -m sheets_airtable_sync.cli health --json ;;
  validate) read -r input mapping <<<"$(scenario_to_paths "${1:-crm-leads}")"; python -m sheets_airtable_sync.cli validate "$input" --mapping "$mapping" ;;
  preview) read -r input mapping <<<"$(scenario_to_paths "${1:-crm-leads}")"; python -m sheets_airtable_sync.cli plan-upserts "$input" --mapping "$mapping" ;;
  report) scenario="${1:-crm-leads}"; read -r input mapping <<<"$(scenario_to_paths "$scenario")"; python -m sheets_airtable_sync.cli report "$input" --mapping "$mapping" --format md --output "examples/output/${scenario}-executor-report.md" ;;
  api-smoke) python - <<'PY'
from fastapi.testclient import TestClient
from sheets_airtable_sync.api import app
c=TestClient(app)
assert c.get('/health').status_code == 200
assert c.post('/sync/preview', json={'input_path':'examples/input/crm-leads.json','mapping_path':'configs/mappings/leads-to-airtable.json'}).status_code == 200
print('{"ok":true,"api_smoke":true,"fixture_safe":true,"live_services_used":false}')
PY
    ;;
  verify)
    python scripts/verify_examples.py >/tmp/sheets-airtable-sync-examples.json
    python -m pytest -q
    python -m ruff check .
    python -m mypy src
    python -m json.tool repo-metadata.json >/dev/null
    echo '{"ok":true,"verified":true,"fixture_safe":true,"live_services_used":false}'
    ;;
  *) echo "usage: ./executor.sh {health|validate|preview|report|api-smoke|verify} [scenario]"; exit 2 ;;
esac
