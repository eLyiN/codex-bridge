# Codex Bridge

![CI Status](https://github.com/eLyiN/codex-bridge/actions/workflows/ci.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/codex-bridge)
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP Compatible](https://img.shields.io/badge/MCP-compatible-green.svg)
![Codex CLI](https://img.shields.io/badge/Codex-CLI-blue.svg)

A lightweight MCP (Model Context Protocol) server that enables AI coding assistants to interact with OpenAI's Codex AI through the official CLI. Works with Claude Code, Cursor, VS Code, and other MCP-compatible clients. Designed for simplicity, reliability, and seamless integration.

## ✨ Features

- **Direct Codex CLI Integration**: Zero API costs using official Codex CLI
- **Simple MCP Tools**: Two core functions for basic queries and file analysis
- **Stateless Operation**: No sessions, caching, or complex state management
- **Production Ready**: Robust error handling with configurable timeouts (default: 90 seconds)
- **Minimal Dependencies**: Only requires `mcp>=1.0.0` and Codex CLI
- **Easy Deployment**: Support for both uvx and traditional pip installation
- **Universal MCP Compatibility**: Works with any MCP-compatible AI coding assistant

## 🚀 Quick Start

### Prerequisites

1. **Install Codex CLI**:
   ```bash
   npm install -g @openai/codex-cli
   ```

2. **Authenticate with Codex**:
   ```bash
   codex
   ```

3. **Verify installation**:
   ```bash
   codex --version
   ```

### Installation

**🎯 Recommended: PyPI Installation**
```bash
# Install from PyPI
pip install codex-bridge

# Add to Claude Code with uvx (recommended)
claude mcp add codex-bridge -s user -- uvx codex-bridge
```

**Alternative: From Source**
```bash
# Clone the repository
git clone https://github.com/shelakh/codex-bridge.git
cd codex-bridge

# Build and install locally
uvx --from build pyproject-build
pip install dist/*.whl

# Add to Claude Code
claude mcp add codex-bridge -s user -- uvx codex-bridge
```

**Development Installation**
```bash
# Clone and install in development mode
git clone https://github.com/shelakh/codex-bridge.git
cd codex-bridge
pip install -e .

# Add to Claude Code (development)
claude mcp add codex-bridge-dev -s user -- python -m src
```

## 🌐 Multi-Client Support

**Codex Bridge works with any MCP-compatible AI coding assistant** - the same server supports multiple clients through different configuration methods.

### Supported MCP Clients
- **Claude Code** ✅ (Default)
- **Cursor** ✅
- **VS Code** ✅
- **Windsurf** ✅
- **Cline** ✅
- **Void** ✅
- **Cherry Studio** ✅
- **Augment** ✅
- **Roo Code** ✅
- **Zencoder** ✅
- **Any MCP-compatible client** ✅

### Configuration Examples

<details>
<summary><strong>Claude Code</strong> (Default)</summary>

```bash
# Recommended installation
claude mcp add codex-bridge -s user -- uvx codex-bridge

# Development installation
claude mcp add codex-bridge-dev -s user -- python -m src
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

**Global Configuration** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

**Project-Specific** (`.cursor/mcp.json` in your project):
```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

Go to: `Settings` → `Cursor Settings` → `MCP` → `Add new global MCP server`

</details>

<details>
<summary><strong>VS Code</strong></summary>

**Configuration** (`.vscode/mcp.json` in your workspace):
```json
{
  "servers": {
    "codex-bridge": {
      "type": "stdio",
      "command": "uvx",
      "args": ["codex-bridge"]
    }
  }
}
```

**Alternative: Through Extensions**
1. Open Extensions view (Ctrl+Shift+X)
2. Search for MCP extensions
3. Add custom server with command: `uvx codex-bridge`

</details>

<details>
<summary><strong>Windsurf</strong></summary>

Add to your Windsurf MCP configuration:
```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary><strong>Cline</strong> (VS Code Extension)</summary>

1. Open Cline and click **MCP Servers** in the top navigation
2. Select **Installed** tab → **Advanced MCP Settings**
3. Add to `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary><strong>Void</strong></summary>

Go to: `Settings` → `MCP` → `Add MCP Server`

```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary><strong>Cherry Studio</strong></summary>

1. Navigate to **Settings → MCP Servers → Add Server**
2. Fill in the server details:
   - **Name**: `codex-bridge`
   - **Type**: `STDIO`
   - **Command**: `uvx`
   - **Arguments**: `["codex-bridge"]`
3. Save the configuration

</details>

<details>
<summary><strong>Augment</strong></summary>

**Using the UI:**
1. Click hamburger menu → **Settings** → **Tools**
2. Click **+ Add MCP** button
3. Enter command: `uvx codex-bridge`
4. Name: **Codex Bridge**

**Manual Configuration:**
```json
"augment.advanced": { 
  "mcpServers": [ 
    { 
      "name": "codex-bridge", 
      "command": "uvx", 
      "args": ["codex-bridge"],
      "env": {}
    }
  ]
}
```

</details>

<details>
<summary><strong>Roo Code</strong></summary>

1. Go to **Settings → MCP Servers → Edit Global Config**
2. Add to `mcp_settings.json`:

```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary><strong>Zencoder</strong></summary>

1. Go to Zencoder menu (...) → **Tools** → **Add Custom MCP**
2. Add configuration:

```json
{
  "command": "uvx",
  "args": ["codex-bridge"],
  "env": {}
}
```

3. Hit the **Install** button

</details>

<details>
<summary><strong>Alternative Installation Methods</strong></summary>

**For pip-based installations:**
```json
{
  "command": "codex-bridge",
  "args": [],
  "env": {}
}
```

**For development/local testing:**
```json
{
  "command": "python",
  "args": ["-m", "src"],
  "env": {},
  "cwd": "/path/to/codex-bridge"
}
```

**For npm-style installation** (if needed):
```json
{
  "command": "npx",
  "args": ["codex-bridge"],
  "env": {}
}
```

</details>

### Universal Usage

Once configured with any client, use the same two tools:

1. **Ask general questions**: "What authentication patterns are used in this codebase?"
2. **Analyze specific files**: "Review these auth files for security issues"

**The server implementation is identical** - only the client configuration differs!

## ⚙️ Configuration

### Timeout Configuration

By default, Codex Bridge uses a 90-second timeout for all CLI operations. For longer queries (large files, complex analysis), you can configure a custom timeout using the `CODEX_TIMEOUT` environment variable.

**Example configurations:**

<details>
<summary><strong>Claude Code</strong></summary>

```bash
# Add with custom timeout (120 seconds)
claude mcp add codex-bridge -s user --env CODEX_TIMEOUT=120 -- uvx codex-bridge
```

</details>

<details>
<summary><strong>Manual Configuration (mcp_settings.json)</strong></summary>

```json
{
  "mcpServers": {
    "codex-bridge": {
      "command": "uvx",
      "args": ["codex-bridge"],
      "env": {
        "CODEX_TIMEOUT": "120"
      }
    }
  }
}
```

</details>

**Timeout Options:**
- **Default**: 90 seconds (if not configured)
- **Range**: Any positive integer (seconds)
- **Recommended**: 60-120 seconds for most queries, 120-300 for large file analysis
- **Invalid values**: Fall back to 90 seconds with warning

## 🛠️ Available Tools

### `consult_codex`
Direct CLI bridge for simple queries with structured JSON output by default.

**Parameters:**
- `query` (string): The question or prompt to send to Codex
- `directory` (string): Working directory for the query (default: current directory)
- `format` (string): Output format - "text", "json", or "code" (default: "json")
- `timeout` (int, optional): Timeout in seconds (recommended: 60-120, default: 90)

**Example:**
```python
consult_codex(
    query="Find authentication patterns in this codebase",
    directory="/path/to/project",
    format="json",  # Default format
    timeout=90      # Default timeout
)
```

### `consult_codex_with_stdin`
CLI bridge with stdin content for pipeline-friendly execution.

**Parameters:**
- `stdin_content` (string): Content to pipe as stdin (file contents, diffs, logs)
- `prompt` (string): The prompt to process the stdin content
- `directory` (string): Working directory for the query
- `format` (string): Output format - "text", "json", or "code" (default: "json")
- `timeout` (int, optional): Timeout in seconds (recommended: 60-120, default: 90)

### `consult_codex_batch`
Batch processing for multiple queries - perfect for CI/CD automation.

**Parameters:**
- `queries` (list): List of query dictionaries with 'query' and optional 'timeout'
- `directory` (string): Working directory for all queries
- `format` (string): Output format - currently only "json" supported for batch

**Example:**
```python
consult_codex_with_stdin(
    stdin_content=open("src/auth.py").read(),
    prompt="Analyze this auth file and suggest improvements",
    directory="/path/to/project",
    format="json",  # Default format
    timeout=120     # Custom timeout for complex analysis
)
```

## 📋 Usage Examples

### Basic Code Analysis
```python
# Simple research query
consult_codex(
    query="What authentication patterns are used in this project?",
    directory="/Users/dev/my-project"
)
```

### Detailed File Review
```python
# Analyze specific files
with open("/Users/dev/my-project/src/auth.py") as f:
    auth_content = f.read()
    
consult_codex_with_stdin(
    stdin_content=auth_content,
    prompt="Review this file and suggest security improvements",
    directory="/Users/dev/my-project",
    format="json",  # Structured output
    timeout=120     # Allow more time for detailed analysis
)
```

### Batch Processing
```python
# Process multiple queries at once
consult_codex_batch(
    queries=[
        {"query": "Analyze authentication patterns", "timeout": 60},
        {"query": "Review database implementations", "timeout": 90},
        {"query": "Check security vulnerabilities", "timeout": 120}
    ],
    directory="/Users/dev/my-project",
    format="json"  # Always JSON for batch processing
)
```

## 🏗️ Architecture

### Core Design
- **CLI-First**: Direct subprocess calls to `codex` command
- **Stateless**: Each tool call is independent with no session state
- **Configurable Timeout**: 90-second default execution time (configurable)
- **Structured Output**: JSON format by default for better integration
- **Simple Error Handling**: Clear error messages with fail-fast approach

### Project Structure
```
codex-bridge/
├── src/
│   ├── __init__.py              # Entry point
│   ├── __main__.py              # Module execution entry point
│   └── mcp_server.py            # Main MCP server implementation
├── .github/                     # GitHub templates and workflows
├── pyproject.toml              # Python package configuration
├── README.md                   # This file
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Community standards
├── SECURITY.md                 # Security policies
├── CHANGELOG.md               # Version history
└── LICENSE                    # MIT license
```

## 🔧 Development

### Local Testing
```bash
# Install in development mode
pip install -e .

# Run directly
python -m src

# Test CLI availability
codex --version
```

### Integration with Claude Code
The server automatically integrates with Claude Code when properly configured through the MCP protocol.

## 🔍 Troubleshooting

### CLI Not Available
```bash
# Install Codex CLI
npm install -g @openai/codex-cli

# Authenticate
codex auth login

# Test
codex --version
```

### Connection Issues
- Verify Codex CLI is properly authenticated
- Check network connectivity
- Ensure Claude Code MCP configuration is correct
- Check that the `codex` command is in your PATH

### Common Error Messages
- **"CLI not available"**: Codex CLI is not installed or not in PATH
- **"Authentication required"**: Run `codex auth login`
- **"Timeout after X seconds"**: Query took too long, try increasing timeout or breaking into smaller parts

## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

### Quick Contributing Guide
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 🆘 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/shelakh/codex-bridge/issues)
- **Discussions**: Join the community discussion
- **Documentation**: Additional docs can be created in the `docs/` directory

---

**Focus**: A simple, reliable bridge between Claude Code and Codex AI through the official CLI.