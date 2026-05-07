# MCP Tool Surface

`src/sheets_airtable_sync/mcp_server.py` exposes pure Python tool functions and builds a FastMCP server when the optional `mcp` package is installed.

Tools:

- `get_sheets_airtable_health`
- `list_sheets_airtable_scenarios`
- `validate_sheets_airtable_rows`
- `plan_airtable_upserts`
- `render_sync_report`

No global Hermes/MCP config is modified by this repo. Automation Kit can register this sector later using the same tool functions.
