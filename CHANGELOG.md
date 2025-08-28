# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-28

### Added

#### Core Features
- **MCP Server Implementation**: Complete Model Context Protocol server for bridging Claude Code to Codex AI
- **Two MCP Tools**:
  - `consult_codex`: Direct CLI bridge for simple queries with optional model selection
  - `consult_codex_with_files`: CLI bridge with file attachment support for detailed analysis
- **CLI Integration**: Direct integration with OpenAI's official Codex CLI
- **Model Support**: Support for Codex models

#### Architecture & Design
- **Stateless Operation**: No session management, caching, or complex state
- **Fixed Timeout**: 60-second maximum execution time for all operations
- **Simple Error Handling**: Clear error messages with fail-fast approach
- **Minimal Dependencies**: Only requires `mcp>=1.0.0` and external Codex CLI

#### Deployment & Installation
- **uvx Support**: Production deployment via uvx with built wheel
- **Development Mode**: Traditional pip installation for development
- **Startup Scripts**: 
  - `start_server_uvx.sh` for production
  - `start_server_dev.sh` for development
- **Package Configuration**: Complete pyproject.toml with metadata and entry points

#### Documentation
- **Comprehensive README**: Installation, usage examples, troubleshooting
- **Contributing Guidelines**: Development setup, code style, PR process
- **Security Policy**: Vulnerability reporting, best practices, update process
- **License**: MIT License for open source use

#### Developer Experience
- **Claude Code Integration**: Seamless MCP protocol integration
- **Error Diagnostics**: Clear error messages for common issues
- **Development Tools**: Easy local testing and development setup

### Technical Details

#### Dependencies
- **Required**: `mcp>=1.0.0`
- **External**: Codex CLI (npm package `@openai/codex-cli`)
- **Python**: Compatible with Python 3.9+

#### File Structure
```
codex-bridge/
├── src/
│   ├── __init__.py              # Package entry point and version
│   ├── __main__.py              # Module execution entry point  
│   └── mcp_server.py            # Core MCP server implementation
├── start_server_uvx.sh         # Production startup script
├── start_server_dev.sh         # Development startup script
├── pyproject.toml              # Python package configuration
└── [documentation files]       # README, CONTRIBUTING, SECURITY, etc.
```

#### Configuration
- **Default Model**: Codex model for optimal performance
- **Timeout**: 60 seconds for all CLI operations
- **Working Directory**: Configurable per request
- **File Encoding**: UTF-8 with error handling

### Security Considerations
- **Input Validation**: Basic validation for file paths and queries
- **Process Isolation**: Subprocess execution for CLI calls
- **No Network Exposure**: All network requests handled by Codex CLI
- **Minimal Attack Surface**: Simple, stateless architecture

### Performance Characteristics
- **Startup Time**: Near-instant MCP server startup
- **Memory Usage**: Minimal memory footprint
- **Execution Time**: Limited by 60-second timeout
- **Scalability**: Stateless design allows multiple concurrent requests

---

## Release Notes

### Version 1.0.0 Highlights

This initial release establishes Codex Bridge as a production-ready MCP server with a focus on:

1. **Simplicity**: Straightforward architecture that's easy to understand and maintain
2. **Reliability**: Robust error handling and fixed timeout protection  
3. **Integration**: Seamless Claude Code integration via MCP protocol
4. **Performance**: Direct CLI integration for optimal speed and cost efficiency
5. **Community**: Complete open source documentation and contribution guidelines

### Migration Notes

This is the initial public release, so no migration is required. Future versions will include migration guidance here.

### Breaking Changes

None in this initial release. Future breaking changes will be clearly documented here.

### Deprecation Warnings

None in this initial release. Future deprecations will be announced here with migration timelines.

---

## Contributors

Special thanks to all contributors who made this release possible:

- **Core Development**: Project architecture and implementation
- **Documentation**: Comprehensive documentation and examples
- **Testing**: Manual testing across different environments
- **Community**: Feedback and suggestions for improvement

## Links

- **Repository**: [https://github.com/shelakh/codex-bridge](https://github.com/shelakh/codex-bridge)
- **Issues**: [https://github.com/shelakh/codex-bridge/issues](https://github.com/shelakh/codex-bridge/issues)
- **MCP Protocol**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **Codex CLI**: [https://www.npmjs.com/package/@openai/codex-cli](https://www.npmjs.com/package/@openai/codex-cli)