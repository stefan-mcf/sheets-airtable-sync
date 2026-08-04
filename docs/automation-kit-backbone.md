# Automation Kit Backbone

This repository is a concrete workflow implementation, not the reusable runtime. It reports optional backbone status via `sheets_airtable_sync.backbone.get_health()`.

The status contract intentionally mirrors sibling repositories:

- `automation_kit_available`
- `fixture_safe=true`
- `live_services_used=false`
- `synthetic_data_only=true`

Upstream Automation Kit registry changes are a separate gate after this sector is green.
