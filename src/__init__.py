"""
MCP Codex Assistant - Simple CLI bridge to OpenAI Codex.
Version 1.2.4 - MCP SDK 2.x compatibility (FastMCP renamed to MCPServer).
"""

from .mcp_server import main

__version__ = "1.2.4"
__all__ = ["main"]