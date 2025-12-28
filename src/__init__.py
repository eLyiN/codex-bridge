"""
MCP Codex Assistant - Simple CLI bridge to OpenAI Codex.
Version 1.2.3 - Windows UTF-8 encoding fix for international character support.
"""

from .mcp_server import main

__version__ = "1.2.3"
__all__ = ["main"]