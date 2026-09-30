#!/usr/bin/env python3
"""
Regression test for the MCP SDK 2.x migration (FastMCP -> MCPServer)

Runs an offline, in-process MCP initialize handshake against the real server
object from src.mcp_server and lists its tools. No network access and no
Codex CLI invocation is performed.
"""

import asyncio
import pathlib
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from mcp import Client

from src.mcp_server import mcp

EXPECTED_TOOLS = {
    "consult_codex",
    "consult_codex_with_stdin",
    "consult_codex_batch",
}

TIMEOUT_SECONDS = 30.0

handshake_ok = True

def check(label: str, condition: bool, detail: str = "") -> None:
    """Record one assertion result and print it."""
    global handshake_ok
    if condition:
        print(f"✅ {label}")
    else:
        handshake_ok = False
        print(f"❌ {label}" + (f": {detail}" if detail else ""))


async def run_handshake() -> None:
    """Complete a real initialize handshake and list the server's tools."""
    print("🧪 Running in-process MCP initialize handshake...")
    async with Client(mcp, mode="legacy") as client:
        server_info = client.server_info
        print(f"🧪 serverInfo: name={server_info.name!r} version={server_info.version!r}")
        print(f"🧪 protocol version: {client.protocol_version}")
        check("handshake succeeded with serverInfo.name == 'codex-assistant'",
              server_info.name == "codex-assistant", f"got {server_info.name!r}")

        tools_result = await client.list_tools()
        tool_names = {tool.name for tool in tools_result.tools}
        print(f"🧪 Listed tools: {sorted(tool_names)}")
        check("tool list is exactly the expected three consult tools",
              tool_names == EXPECTED_TOOLS,
              f"expected {sorted(EXPECTED_TOOLS)}, got {sorted(tool_names)}")


def main() -> None:
    """Run the handshake regression test with a hard timeout."""
    print("🚀 Starting MCP handshake regression test")
    print("=" * 50)

    start = time.monotonic()
    try:
        asyncio.run(asyncio.wait_for(run_handshake(), timeout=TIMEOUT_SECONDS))
    except Exception as exc:  # noqa: BLE001 - script-style test, report and fail
        global handshake_ok
        handshake_ok = False
        print(f"❌ Handshake failed: {exc!r}")

    elapsed = time.monotonic() - start
    print(f"🧪 Elapsed: {elapsed:.2f}s")
    check(f"handshake completed well under 60 seconds (took {elapsed:.2f}s)",
          elapsed < 60.0)

    if handshake_ok:
        print("🎉 MCP handshake regression test passed!")
        sys.exit(0)
    else:
        print("💥 MCP handshake regression test failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()