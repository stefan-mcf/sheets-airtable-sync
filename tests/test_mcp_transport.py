"""Protocol and file-boundary coverage for the optional MCP adapter."""

import asyncio
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

from sheets_airtable_sync.mcp_server import plan_airtable_upserts

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("input_path", ["../README.md", "/etc/hosts"])
def test_mcp_rejects_files_outside_bundled_input(input_path: str) -> None:
    with pytest.raises(ValueError, match="bundled files"):
        plan_airtable_upserts(input_path, "configs/mappings/leads-to-airtable.json")


def test_stdio_discovery_preview_and_rejection() -> None:
    async def probe() -> None:
        server = StdioServerParameters(
            command=sys.executable,
            args=["-m", "sheets_airtable_sync.mcp_server"],
            cwd=str(ROOT),
            env={"PYTHONPATH": str(ROOT / "src")},
        )
        async with asyncio.timeout(30):
            async with stdio_client(server) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    initialized = await session.initialize()
                    assert initialized.server_info.name == "sheets-airtable-sync"
                    tools = await session.list_tools()
                    assert "plan_airtable_upserts" in {tool.name for tool in tools.tools}
                    preview = await session.call_tool(
                        "plan_airtable_upserts",
                        {
                            "input_path": "examples/input/crm-leads.json",
                            "mapping_path": "configs/mappings/leads-to-airtable.json",
                        },
                    )
                    assert not preview.is_error
                    data = json.loads(preview.content[0].text)
                    assert data["airtable_upserts"]
                    assert data["live_services_used"] is False
                    rejected = await session.call_tool(
                        "plan_airtable_upserts",
                        {
                            "input_path": "../README.md",
                            "mapping_path": "configs/mappings/leads-to-airtable.json",
                        },
                    )
                    assert rejected.is_error

    asyncio.run(probe())
