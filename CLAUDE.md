# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Codex Bridge** is a lightweight MCP (Model Context Protocol) server that enables Claude Code to interact with OpenAI's Codex AI through the official CLI. The project follows extreme simplicity principles from Carmack and Torvalds - doing ONE thing well: bridging Claude to Codex CLI.

**Key Characteristics:**
- Non-interactive execution with structured output formats (text, JSON, code)
- Stateless architecture with no session management
- Direct subprocess integration for optimal performance
- Batch processing support for CI/CD workflows
- Pipeline-friendly stdin support

## Development Commands

### Prerequisites
- **Codex CLI**: Install from OpenAI (official CLI)
- **Authentication**: Setup OpenAI API credentials
- **Verify**: `codex --version`

### Installation & Setup

**Development Mode:**
```bash
# Clone and install in development mode
git clone https://github.com/shelakh/codex-bridge.git
cd codex-bridge
pip install -e .

# Run directly from source
python -m src
```

**Production Installation:**
```bash
# Install from PyPI
pip install codex-bridge

# Or use uvx (recommended)
uvx codex-bridge
```

**Claude Code Integration:**
```bash
# Production installation (recommended)
claude mcp add codex-bridge -s user -- uvx codex-bridge

# Development mode (from local source)
claude mcp add codex-bridge -s user -- python -m src
```

### Testing & Verification
```bash
# Test CLI availability
codex --version

# Test basic functionality
python -c "from src.mcp_server import execute_codex_prompt; print('MCP server loaded successfully')"

# Test package installation
python -c "import src; print(f'Codex Bridge v{src.__version__}')"
```

### Build & Distribution
```bash
# Clean build
rm -rf dist/ build/ *.egg-info

# Build package
uvx --from build pyproject-build

# Verify build
pip install dist/*.whl
python -c "import src; print('Package works!')"
```

## Architecture

### Core Design Principles
- **CLI-First**: Direct subprocess calls to `codex` command
- **Stateless**: Each tool call is independent with no session state
- **Non-Interactive**: Structured execution with JSON/text/code formats
- **Configurable Timeout**: Default 90-second execution time (configurable via CODEX_TIMEOUT)
- **Git Repository Check**: Configurable via CODEX_SKIP_GIT_CHECK for non-git directories
- **Fail-Fast**: Clear error messages with simple error handling
- **Zero Dependencies**: Only `mcp>=1.0.0` and external Codex CLI

### Key Components

**`src/mcp_server.py`** - Main server implementation
- `consult_codex(query, directory, format, timeout)` - Non-interactive consultation
- `consult_codex_with_stdin(stdin_content, prompt, directory, format, timeout)` - Pipeline consultation
- `consult_codex_batch(queries, directory, format)` - Batch processing
- `_format_response()` - Output formatting for text/JSON/code

**Codex CLI Integration:**
- Uses the official OpenAI Codex CLI without model selection
- Single unified interface for AI-powered code assistance

### File Structure
```
codex-bridge/
├── src/
│   ├── __init__.py              # Package entry point and version
│   ├── __main__.py              # Module execution entry point  
│   └── mcp_server.py            # Main MCP server implementation
├── .github/                     # GitHub templates and workflows
├── pyproject.toml               # Python package configuration
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Development guidelines
├── SECURITY.md                  # Security policy
├── CHANGELOG.md                 # Release history
└── LICENSE                      # MIT license
```

## MCP Tools Available

### `consult_codex`
- **Purpose**: Non-interactive Codex consultation with structured output
- **Parameters**: 
  - `query` (required): The prompt to send to Codex
  - `directory` (required): Working directory for the query
  - `format` (optional): Output format - "text", "json", or "code" (default: "text")
  - `timeout` (optional): Timeout in seconds (overrides env var)
- **Use Case**: Direct code generation, analysis, structured responses
- **Example**: Code completion, refactoring suggestions

### `consult_codex_with_stdin` 
- **Purpose**: Pipeline-friendly consultation with stdin content
- **Parameters**: 
  - `stdin_content` (required): Content to pipe (file contents, diffs, logs)
  - `prompt` (required): The prompt to process the stdin content
  - `directory` (required): Working directory for the query  
  - `format` (optional): Output format - "text", "json", or "code" (default: "text")
  - `timeout` (optional): Timeout in seconds (overrides env var)
- **Use Case**: CI/CD workflows, processing file contents, diff analysis
- **Example**: Code reviews, log analysis, file processing

### `consult_codex_batch`
- **Purpose**: Batch processing for multiple queries - CI/CD automation
- **Parameters**: 
  - `queries` (required): List of query dictionaries with 'query' and optional 'timeout'
  - `directory` (required): Working directory for all queries
  - `format` (optional): Output format - currently only "json" supported
- **Use Case**: Bulk operations, automated testing, batch analysis
- **Example**: Multiple code reviews, batch refactoring, automated QA

## Error Handling & Troubleshooting

### Common Error Patterns
- **"CLI not available"**: Codex CLI not installed or not in PATH
  - Solution: Install official Codex CLI from OpenAI
- **"Authentication required"**: Not authenticated with OpenAI
  - Solution: Setup OpenAI API credentials
- **"Timeout after X seconds"**: Query too complex or model overloaded
  - Solution: Increase timeout with CODEX_TIMEOUT environment variable
  - Alternative: Break into smaller parts or use batch processing
- **"Not inside a trusted directory"**: Git repository check failed
  - Solution: Set CODEX_SKIP_GIT_CHECK=true environment variable (use only in trusted directories)
- **"Directory does not exist"**: Invalid directory parameter
  - Solution: Use absolute paths or verify directory exists
- **"Invalid format"**: Unsupported format parameter
  - Solution: Use "text", "json", or "code" formats only

### Debugging Steps
1. **Verify Codex CLI**: `codex --version`
2. **Test Authentication**: `codex "Hello World"`
3. **Check Package**: `python -c "import src; print('OK')"`
4. **Test MCP Tools**: Use simple queries first, then add complexity

## Development Guidelines

### Code Standards
- **Python 3.10+ Compatibility**: Use modern Python features responsibly
- **Type Hints**: Include type annotations for all functions
- **Error Handling**: Explicit error messages with actionable solutions
- **Documentation**: Keep CLAUDE.md, README.md, and code comments in sync

### Testing Requirements
- **Manual Testing**: Verify all three MCP tools work with various queries
- **Integration Testing**: Test with Claude Code in development
- **Cross-Platform**: Ensure compatibility across Python versions (3.10-3.12)
- **CI/CD Verification**: All GitHub Actions must pass

### Performance Characteristics
- **Startup Time**: Near-instant MCP server startup
- **Memory Usage**: Minimal memory footprint (~10MB)
- **Execution Time**: Limited by configurable timeout (default: 60 seconds)
- **Scalability**: Stateless design allows multiple concurrent requests

## Package Information

### Dependencies
- **Required**: `mcp>=1.0.0`
- **External**: Codex CLI (official OpenAI CLI)
- **Python**: Compatible with Python 3.10+

### Installation Details
- **Package Name**: `codex-bridge`
- **PyPI**: Available as `pip install codex-bridge`
- **Entry Point**: `codex-bridge = "src:main"`
- **Module Execution**: `python -m src`

### Configuration
- **Timeout**: Configurable via CODEX_TIMEOUT environment variable (default: 90 seconds)
- **Git Repository Check**: Configurable via CODEX_SKIP_GIT_CHECK environment variable (default: enabled)
- **Working Directory**: Configurable per request
- **File Encoding**: UTF-8 with error handling

#### Environment Variables
Set environment variables to customize behavior:

```bash
# Example: 2-minute timeout configuration
claude mcp add codex-bridge -s user --env CODEX_TIMEOUT=120 -- uvx codex-bridge

# Example: Enable for non-git directories (use only in trusted environments)
claude mcp add codex-bridge -s user --env CODEX_SKIP_GIT_CHECK=true -- uvx codex-bridge

# Example: Both configurations
claude mcp add codex-bridge -s user --env CODEX_TIMEOUT=120 --env CODEX_SKIP_GIT_CHECK=true -- uvx codex-bridge
```

**Valid Variables:**
- **CODEX_TIMEOUT**: Positive integers (seconds), default: 90
  - **Recommended**: 120-300 seconds timeout for complex queries
- **CODEX_SKIP_GIT_CHECK**: Boolean-like values ("true", "1", "yes"), default: false
  - **Security Warning**: Only use in trusted directories you control
  - **Use case**: Working in directories that are not Git repositories

## Security Considerations

### Secure Practices
- **Input Validation**: Basic validation for queries and parameters
- **Process Isolation**: Subprocess execution for CLI calls
- **No Network Exposure**: All network requests handled by Codex CLI
- **Minimal Attack Surface**: Simple, stateless architecture

### Best Practices
- Keep Codex CLI updated to latest version
- Use absolute paths for file operations
- Validate directory permissions before operations
- Monitor for unusual CLI behavior or errors

## Release & Deployment

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Current Version**: 1.0.0 (check `src/__init__.py`)
- **Release Tags**: Git tags trigger automated PyPI publishing

### Deployment Options
1. **PyPI + uvx** (Recommended): `uvx codex-bridge`
2. **PyPI + pip**: `pip install codex-bridge`
3. **Development**: `python -m src` from source

### CI/CD Pipeline
- **GitHub Actions**: Automated testing on Python 3.10-3.12
- **PyPI Publishing**: Triggered by version tags (v*.*)
- **Quality Gates**: Build verification, import testing, package validation

## Support & Community

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/shelakh/codex-bridge/issues)
- **Documentation**: README.md, CONTRIBUTING.md, SECURITY.md
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io/)

### Contributing
- **Guidelines**: See CONTRIBUTING.md for detailed development setup
- **Code Style**: Follow PEP 8, use type hints, include docstrings
- **Testing**: Manual testing required, automated CI verification
- **Community**: Respectful, constructive feedback welcome

---

This CLAUDE.md file serves as the authoritative development guide for the Codex Bridge project. Keep it updated as the project evolves, ensuring consistency with README.md, CONTRIBUTING.md, and actual implementation.