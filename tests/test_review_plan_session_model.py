import json
import subprocess
import sys
import types
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

# Provide a minimal FastMCP stub for environments where mcp.server.fastmcp
# isn't available (matches current CI behavior in this repository).
if "mcp.server.fastmcp" not in sys.modules:
    mcp_module = types.ModuleType("mcp")
    server_module = types.ModuleType("mcp.server")
    fastmcp_module = types.ModuleType("mcp.server.fastmcp")

    class FastMCP:  # type: ignore[too-many-ancestors]
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def tool(self):
            def decorator(func):
                return func
            return decorator

        def run(self) -> None:
            return None

    fastmcp_module.FastMCP = FastMCP
    mcp_module.server = server_module
    server_module.fastmcp = fastmcp_module
    sys.modules["mcp"] = mcp_module
    sys.modules["mcp.server"] = server_module
    sys.modules["mcp.server.fastmcp"] = fastmcp_module

from src.mcp_server import review_plan


def _success(stdout: str = "ok") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=["codex", "exec"],
        returncode=0,
        stdout=stdout,
        stderr=""
    )


def _failure(stderr: str) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=["codex", "exec"],
        returncode=1,
        stdout="",
        stderr=stderr
    )


def test_review_plan_continuation_keeps_configured_model() -> None:
    with TemporaryDirectory() as temp_dir:
        config = Path(temp_dir) / ".reviewbridge.json"
        config.write_text('{"model":"gpt-5.4"}', encoding="utf-8")

        with patch("src.mcp_server._get_codex_command", return_value="codex"), patch(
            "src.mcp_server._run_codex_command", return_value=_success("review ok")
        ) as run_command:
            result = review_plan(
                prompt="Create a plan",
                directory=temp_dir,
                session_id="session-123",
                format="json"
            )

        cmd = run_command.call_args.args[0]
        assert "--session" in cmd
        assert "session-123" in cmd
        assert "--model" in cmd
        assert cmd[cmd.index("--model") + 1] == "gpt-5.4"

        parsed = json.loads(result)
        assert parsed["metadata"]["model"] == "gpt-5.4"
        assert parsed["metadata"]["session_id"] == "session-123"


def test_review_plan_falls_back_to_fresh_session_when_chatgpt_continuation_model_fails() -> None:
    model_error = (
        '{"type":"invalid_request_error","message":"The \'gpt-5.3-codex\' model is not '
        'supported when using Codex with a ChatGPT account."}'
    )

    with TemporaryDirectory() as temp_dir:
        with patch("src.mcp_server._get_codex_command", return_value="codex"), patch(
            "src.mcp_server._run_codex_command",
            side_effect=[_failure(model_error), _success("fallback ok")]
        ) as run_command:
            result = review_plan(
                prompt="Continue planning",
                directory=temp_dir,
                session_id="session-456",
                model="gpt-5.4",
                format="json"
            )

        first_cmd = run_command.call_args_list[0].args[0]
        second_cmd = run_command.call_args_list[1].args[0]

        assert "--session" in first_cmd
        assert "session-456" in first_cmd
        assert "--session" not in second_cmd
        assert "--model" in second_cmd
        assert second_cmd[second_cmd.index("--model") + 1] == "gpt-5.4"

        parsed = json.loads(result)
        assert parsed["metadata"]["fallback_used"] is True
        assert parsed["metadata"]["fallback_reason"] == "session_continuation_model_unavailable"
        assert parsed["metadata"]["original_session_id"] == "session-456"
