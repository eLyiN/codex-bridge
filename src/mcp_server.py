#!/usr/bin/env python3
"""
Codex MCP Server - Simple CLI Bridge
Version 1.2.3
A minimal MCP server to interface with OpenAI Codex via the codex CLI.
Created by @shelakh/elyin

Following Carmack's principle: "Simplicity is prerequisite for reliability"
Following Torvalds' principle: "Good taste in code - knowing what NOT to write"

This server does ONE thing: bridge Claude to Codex CLI. Nothing more.
Non-interactive execution with JSON output and batch processing support.

Windows compatibility: Uses UTF-8 encoding for subprocess I/O to handle
international characters correctly on Windows systems.
"""

import json
import os
import platform
import re
import subprocess
import shutil
import time
from typing import Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("codex-assistant")


def _is_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system().lower() == "windows"


def _get_codex_command() -> Optional[str]:
    """Get the codex command path with Windows compatibility.

    Returns:
        Path to codex executable or None if not found
    """
    # First try the standard shutil.which approach
    codex_path = shutil.which("codex")
    if codex_path:
        return codex_path

    # On Windows, explicitly check for common executable extensions
    if _is_windows():
        for ext in ['.exe', '.bat', '.cmd', '.ps1']:
            codex_path = shutil.which(f"codex{ext}")
            if codex_path:
                return codex_path

        # Also check common installation paths on Windows
        common_paths = [
            os.path.expandvars(r'%LOCALAPPDATA%\Programs\codex\codex.exe'),
            os.path.expandvars(r'%APPDATA%\npm\codex.cmd'),
            os.path.expandvars(r'%USERPROFILE%\.cargo\bin\codex.exe'),
        ]
        for path in common_paths:
            if os.path.isfile(path):
                return path

    return None


def _build_codex_exec_command() -> List[str]:
    """Build the command list to execute codex exec.

    On Windows, if the codex CLI is a PowerShell script (.ps1), we need to
    invoke it through PowerShell explicitly. Otherwise, use the resolved path
    or fall back to 'codex' for PATH resolution.

    Returns:
        Command list suitable for subprocess execution
    """
    codex_path = _get_codex_command()

    if codex_path and _is_windows():
        # Check if it's a PowerShell script
        if codex_path.lower().endswith('.ps1'):
            # Execute PowerShell script: powershell -ExecutionPolicy Bypass -File script.ps1 exec
            return ['powershell', '-ExecutionPolicy', 'Bypass', '-File', codex_path, 'exec']
        else:
            # Use the resolved path directly for .exe, .bat, .cmd
            return [codex_path, 'exec']

    # For Unix or when codex is in PATH, use simple command
    return ['codex', 'exec']


def _get_timeout() -> int:
    """Get timeout from environment variable or default to 90 seconds.
    
    Recommended: 60-120 seconds. Values under 60 may cause hanging.
    """
    try:
        return int(os.environ.get("CODEX_TIMEOUT", "90"))
    except ValueError:
        return 90


def _should_skip_git_check() -> bool:
    """Check if git repository check should be skipped.
    
    Reads CODEX_SKIP_GIT_CHECK environment variable.
    Defaults to False for security. Set to 'true' or '1' to enable.
    """
    skip_check = os.environ.get("CODEX_SKIP_GIT_CHECK", "false").lower()
    return skip_check in ("true", "1", "yes")


def _run_codex_command(cmd: List[str], directory: str, timeout_value: int, input_text: str) -> subprocess.CompletedProcess:
    """Execute codex command with platform-specific handling.

    Args:
        cmd: Command list to execute
        directory: Working directory
        timeout_value: Timeout in seconds
        input_text: Input text to pipe to the command

    Returns:
        CompletedProcess result with stdout/stderr as strings
    """
    # Windows-specific handling with UTF-8 encoding support
    if _is_windows():
        # On Windows, we need to:
        # 1. Use encoding='utf-8' instead of text=True to avoid code page issues
        # 2. Set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 for consistent encoding
        # 3. Don't use start_new_session as it's not supported on Windows
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'

        # Encode input as UTF-8 bytes
        input_bytes = input_text.encode('utf-8') if input_text else None

        result = subprocess.run(
            cmd,
            cwd=directory,
            capture_output=True,
            timeout=timeout_value,
            input=input_bytes,
            shell=False,
            env=env
        )

        # Decode output as UTF-8 with error handling
        return subprocess.CompletedProcess(
            args=result.args,
            returncode=result.returncode,
            stdout=result.stdout.decode('utf-8', errors='replace') if result.stdout else '',
            stderr=result.stderr.decode('utf-8', errors='replace') if result.stderr else ''
        )
    else:
        # Unix/macOS handling (original behavior)
        return subprocess.run(
            cmd,
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=timeout_value,
            input=input_text,
            start_new_session=True
        )


def _clean_codex_output(output: str) -> str:
    """Clean irrelevant messages from Codex CLI output."""
    if not output:
        return output
    
    # Filter out common CLI noise and warnings
    lines = output.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that contain irrelevant CLI messages
        if (line.strip().startswith("Warning:") or
            line.strip().startswith("Note:") or
            line.strip() == ""):
            continue
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()


def _format_prompt_for_json(query: str) -> str:
    """Append JSON format instructions to query for structured output."""
    return f"""{query}

Please respond in valid JSON format with this structure:
- "result": Your detailed answer/response
- "confidence": "high", "medium", or "low"  
- "reasoning": Brief explanation of your analysis

Format your response as valid JSON only."""


def _extract_json_from_response(response: str) -> Optional[Dict]:
    """Extract JSON from mixed text response using regex."""
    # Clean the response to remove CLI noise
    lines = response.split('\n')
    clean_lines = []
    json_started = False
    
    for line in lines:
        # Skip CLI headers and metadata
        if (line.startswith('[') and ']' in line and ('OpenAI' in line or 'workdir:' in line or 'model:' in line)):
            continue
        if line.startswith('--------'):
            continue
        if 'tokens used:' in line:
            continue
        if 'thinking' in line and line.startswith('['):
            continue
        if 'codex' in line and line.startswith('['):
            continue
            
        # Look for JSON content
        if '{' in line:
            json_started = True
        if json_started:
            clean_lines.append(line)
    
    clean_response = '\n'.join(clean_lines)
    
    # Try to find complete JSON objects
    json_pattern = r'\{(?:[^{}]|{[^{}]*})*\}'
    matches = re.findall(json_pattern, clean_response, re.DOTALL)
    
    for match in matches:
        try:
            parsed = json.loads(match.strip())
            # Validate it has expected structure
            if isinstance(parsed, dict) and any(key in parsed for key in ['result', 'response', 'answer']):
                return parsed
        except json.JSONDecodeError:
            continue
    
    return None


def _format_response(raw_response: str, format_type: str, execution_time: float, directory: str) -> str:
    """Format response according to specified output format."""
    if format_type == "text":
        return raw_response
    
    elif format_type == "json":
        # Try to extract JSON from response first
        extracted_json = _extract_json_from_response(raw_response)
        
        if extracted_json:
            # Wrap extracted JSON in standard structure
            return json.dumps({
                "status": "success",
                "response": extracted_json,
                "metadata": {
                    "execution_time": execution_time,
                    "directory": directory,
                    "format": "json"
                }
            }, indent=2)
        else:
            # Fallback: wrap raw response
            return json.dumps({
                "status": "success",
                "response": raw_response,
                "metadata": {
                    "execution_time": execution_time,
                    "directory": directory,
                    "format": "json"
                }
            }, indent=2)
    
    elif format_type == "code":
        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', raw_response, re.DOTALL)
        
        return json.dumps({
            "status": "success",
            "response": raw_response,
            "code_blocks": [{"language": lang or "text", "code": code.strip()} for lang, code in code_blocks],
            "metadata": {
                "execution_time": execution_time,
                "directory": directory,
                "format": "code"
            }
        }, indent=2)
    
    else:
        return raw_response


@mcp.tool()
def consult_codex(
    query: str,
    directory: str,
    format: str = "json",
    timeout: Optional[int] = None
) -> str:
    """
    Consult Codex in non-interactive mode with structured output.
    
    Processes prompt and returns formatted response.
    Supports text, JSON, and code extraction formats.
    
    Args:
        query: The prompt to send to Codex
        directory: Working directory (required)
        format: Output format - "text", "json", or "code" (default: "json")
        timeout: Optional timeout in seconds (overrides env var, recommended: 60-120)
        
    Returns:
        Formatted response based on format parameter
    """
    # Check if codex CLI is available
    if not _get_codex_command():
        error_response = "Error: Codex CLI not found. Install from OpenAI"
        if format == "json":
            return json.dumps({"status": "error", "error": error_response}, indent=2)
        return error_response
    
    # Validate directory
    if not os.path.isdir(directory):
        error_response = f"Error: Directory does not exist: {directory}"
        if format == "json":
            return json.dumps({"status": "error", "error": error_response}, indent=2)
        return error_response
    
    # Validate format
    if format not in ["text", "json", "code"]:
        error_response = f"Error: Invalid format '{format}'. Must be 'text', 'json', or 'code'"
        # Always return JSON for invalid format errors for consistency
        return json.dumps({"status": "error", "error": error_response}, indent=2)
    
    # Prepare query based on format
    if format == "json":
        processed_query = _format_prompt_for_json(query)
    else:
        processed_query = query
    
    # Setup command and timeout
    cmd = _build_codex_exec_command()
    if _should_skip_git_check():
        cmd.append("--skip-git-repo-check")
    timeout_value = timeout or _get_timeout()

    # Execute with timing
    start_time = time.time()
    try:
        result = _run_codex_command(cmd, directory, timeout_value, processed_query)
        execution_time = time.time() - start_time

        if result.returncode == 0:
            cleaned_output = _clean_codex_output(result.stdout)
            raw_response = cleaned_output if cleaned_output else "No output from Codex CLI"
            return _format_response(raw_response, format, execution_time, directory)
        else:
            error_response = f"Codex CLI Error: {result.stderr.strip()}"
            if format == "json":
                return json.dumps({
                    "status": "error",
                    "error": error_response,
                    "metadata": {
                        "execution_time": execution_time,
                        "directory": directory,
                        "format": format
                    }
                }, indent=2)
            return error_response

    except subprocess.TimeoutExpired:
        error_response = f"Error: Codex CLI command timed out after {timeout_value} seconds"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "timeout": timeout_value,
                    "directory": directory,
                    "format": format
                }
            }, indent=2)
        return error_response
    except FileNotFoundError as e:
        # More specific error for when codex command is not found
        codex_path = _get_codex_command()
        if _is_windows():
            error_response = (
                f"Error: Codex CLI not found or not executable. "
                f"Detected path: {codex_path or 'None'}. "
                f"Please ensure 'codex' is installed and in your PATH. "
                f"Try running 'codex --version' in Command Prompt to verify."
            )
        else:
            error_response = f"Error: Codex CLI not found: {str(e)}"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "directory": directory,
                    "format": format,
                    "platform": platform.system()
                }
            }, indent=2)
        return error_response
    except Exception as e:
        error_response = f"Error executing Codex CLI: {str(e)}"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "directory": directory,
                    "format": format,
                    "platform": platform.system(),
                    "exception_type": type(e).__name__
                }
            }, indent=2)
        return error_response


@mcp.tool()
def consult_codex_with_stdin(
    stdin_content: str,
    prompt: str,
    directory: str,
    format: str = "json",
    timeout: Optional[int] = None
) -> str:
    """
    Consult Codex with stdin content piped to prompt - pipeline-friendly execution.
    
    Similar to 'echo "content" | codex exec "prompt"' - combines stdin with prompt.
    Perfect for CI/CD workflows where you pipe file contents to the AI.
    
    Args:
        stdin_content: Content to pipe as stdin (e.g., file contents, diff, logs)
        prompt: The prompt to process the stdin content
        directory: Working directory (required)
        format: Output format - "text", "json", or "code" (default: "json")
        timeout: Optional timeout in seconds (overrides env var, recommended: 60-120)
        
    Returns:
        Formatted response based on format parameter
    """
    # Check if codex CLI is available
    if not _get_codex_command():
        error_response = "Error: Codex CLI not found. Install from OpenAI"
        if format == "json":
            return json.dumps({"status": "error", "error": error_response}, indent=2)
        return error_response
    
    # Validate directory
    if not os.path.isdir(directory):
        error_response = f"Error: Directory does not exist: {directory}"
        if format == "json":
            return json.dumps({"status": "error", "error": error_response}, indent=2)
        return error_response
    
    # Validate format
    if format not in ["text", "json", "code"]:
        error_response = f"Error: Invalid format '{format}'. Must be 'text', 'json', or 'code'"
        # Always return JSON for invalid format errors for consistency
        return json.dumps({"status": "error", "error": error_response}, indent=2)
    
    # Combine stdin content with prompt
    combined_input = f"{stdin_content}\n\n{prompt}"

    # Prepare query based on format
    if format == "json":
        processed_query = _format_prompt_for_json(combined_input)
    else:
        processed_query = combined_input

    # Setup command and timeout
    cmd = _build_codex_exec_command()
    if _should_skip_git_check():
        cmd.append("--skip-git-repo-check")
    timeout_value = timeout or _get_timeout()
    
    # Execute with timing
    start_time = time.time()
    try:
        result = _run_codex_command(cmd, directory, timeout_value, processed_query)
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            cleaned_output = _clean_codex_output(result.stdout)
            raw_response = cleaned_output if cleaned_output else "No output from Codex CLI"
            return _format_response(raw_response, format, execution_time, directory)
        else:
            error_response = f"Codex CLI Error: {result.stderr.strip()}"
            if format == "json":
                return json.dumps({
                    "status": "error",
                    "error": error_response,
                    "metadata": {
                        "execution_time": execution_time,
                        "directory": directory,
                        "format": format
                    }
                }, indent=2)
            return error_response
            
    except subprocess.TimeoutExpired:
        error_response = f"Error: Codex CLI command timed out after {timeout_value} seconds"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "timeout": timeout_value,
                    "directory": directory,
                    "format": format
                }
            }, indent=2)
        return error_response
    except FileNotFoundError as e:
        # More specific error for when codex command is not found
        codex_path = _get_codex_command()
        if _is_windows():
            error_response = (
                f"Error: Codex CLI not found or not executable. "
                f"Detected path: {codex_path or 'None'}. "
                f"Please ensure 'codex' is installed and in your PATH. "
                f"Try running 'codex --version' in Command Prompt to verify."
            )
        else:
            error_response = f"Error: Codex CLI not found: {str(e)}"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "directory": directory,
                    "format": format,
                    "platform": platform.system()
                }
            }, indent=2)
        return error_response
    except Exception as e:
        error_response = f"Error executing Codex CLI: {str(e)}"
        if format == "json":
            return json.dumps({
                "status": "error",
                "error": error_response,
                "metadata": {
                    "directory": directory,
                    "format": format,
                    "platform": platform.system(),
                    "exception_type": type(e).__name__
                }
            }, indent=2)
        return error_response


@mcp.tool()
def consult_codex_batch(
    queries: List[Dict[str, Union[str, int]]],
    directory: str,
    format: str = "json"
) -> str:
    """
    Consult multiple Codex queries in batch - perfect for CI/CD automation.
    
    Processes multiple prompts and returns consolidated JSON output.
    Each query can have individual timeout and format preferences.
    
    Args:
        queries: List of query dictionaries with keys: 'query' (required), 'timeout' (optional)
        directory: Working directory (required)
        format: Output format - currently only "json" supported for batch
        
    Returns:
        JSON array with all results
    """
    # Check if codex CLI is available
    if not _get_codex_command():
        return json.dumps({
            "status": "error",
            "error": "Codex CLI not found. Install from OpenAI"
        }, indent=2)
    
    # Validate directory
    if not os.path.isdir(directory):
        return json.dumps({
            "status": "error",
            "error": f"Directory does not exist: {directory}"
        }, indent=2)
    
    # Validate queries
    if not queries or not isinstance(queries, list):
        return json.dumps({
            "status": "error",
            "error": "Queries must be a non-empty list"
        }, indent=2)
    
    # Force JSON format for batch processing
    format = "json"
    results = []
    
    for i, query_item in enumerate(queries):
        if not isinstance(query_item, dict) or 'query' not in query_item:
            results.append({
                "status": "error",
                "error": f"Query {i+1}: Must be a dictionary with 'query' key",
                "index": i
            })
            continue
        
        query = str(query_item.get('query', ''))
        query_timeout = query_item.get('timeout', _get_timeout())
        if isinstance(query_timeout, str):
            try:
                query_timeout = int(query_timeout)
            except ValueError:
                query_timeout = _get_timeout()
        
        # Process individual query
        processed_query = _format_prompt_for_json(query)
        cmd = _build_codex_exec_command()
        if _should_skip_git_check():
            cmd.append("--skip-git-repo-check")
        
        start_time = time.time()
        try:
            result = _run_codex_command(cmd, directory, query_timeout, processed_query)
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                cleaned_output = _clean_codex_output(result.stdout)
                raw_response = cleaned_output if cleaned_output else "No output from Codex CLI"
                
                # Try to extract JSON from response
                extracted_json = _extract_json_from_response(raw_response)
                
                results.append({
                    "status": "success",
                    "index": i,
                    "query": query[:100] + "..." if len(query) > 100 else query,  # Truncate long queries
                    "response": extracted_json if extracted_json else raw_response,
                    "metadata": {
                        "execution_time": execution_time,
                        "timeout": query_timeout
                    }
                })
            else:
                results.append({
                    "status": "error",
                    "index": i,
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "error": f"Codex CLI Error: {result.stderr.strip()}",
                    "metadata": {
                        "execution_time": execution_time,
                        "timeout": query_timeout
                    }
                })
                
        except subprocess.TimeoutExpired:
            results.append({
                "status": "error",
                "index": i,
                "query": query[:100] + "..." if len(query) > 100 else query,
                "error": f"Query timed out after {query_timeout} seconds",
                "metadata": {
                    "timeout": query_timeout
                }
            })
        except FileNotFoundError as e:
            codex_path = _get_codex_command()
            if _is_windows():
                error_msg = (
                    f"Codex CLI not found or not executable. "
                    f"Detected path: {codex_path or 'None'}. "
                    f"Please ensure 'codex' is installed and in your PATH."
                )
            else:
                error_msg = f"Codex CLI not found: {str(e)}"
            results.append({
                "status": "error",
                "index": i,
                "query": query[:100] + "..." if len(query) > 100 else query,
                "error": error_msg,
                "metadata": {
                    "platform": platform.system()
                }
            })
        except Exception as e:
            results.append({
                "status": "error",
                "index": i,
                "query": query[:100] + "..." if len(query) > 100 else query,
                "error": f"Error executing query: {str(e)}",
                "metadata": {}
            })
    
    # Return consolidated results
    return json.dumps({
        "status": "completed",
        "total_queries": len(queries),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "error"]),
        "results": results,
        "metadata": {
            "directory": directory,
            "format": format
        }
    }, indent=2)


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()