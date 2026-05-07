# Automation Kit Backbone

This repo is a concrete workflow proof, not the reusable runtime. It reports optional backbone status via `sheets_airtable_sync.backbone.get_health()`.

The status contract intentionally mirrors sibling proof repos:

- `automation_kit_available`
- `fixture_safe=true`
- `live_services_used=false`
- `synthetic_data_only=true`

Upstream Automation Kit registry changes are a separate gate after this sector is green.
