# MCP Tool Surface

`src/sheets_airtable_sync/mcp_server.py` exposes Python tool functions and an optional official MCP SDK 2.x stdio server.

```bash
pip install -e '.[dev,mcp]'
python -m sheets_airtable_sync.mcp_server
```

Run `python -m pytest -q tests/test_mcp_transport.py` to exercise actual initialization, tool discovery, upsert preview and rejection. Path-taking tools accept bundled files under `examples/input` and `configs/mappings`; traversal and outside paths are rejected.

The toolkit does not require MCP for CLI/API use. SDK client/server stdio verification does not establish every host or HTTP transport. See the [official SDK](https://github.com/modelcontextprotocol/python-sdk).

Tools:

- `get_sheets_airtable_health`
- `list_sheets_airtable_scenarios`
- `validate_sheets_airtable_rows`
- `plan_airtable_upserts`
- `render_sync_report`

No global Hermes/MCP config is modified by this repo. Automation Kit can register this sector later using the same tool functions.
