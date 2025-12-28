# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.3] - 2025-12-28

### Fixed
- **Windows UTF-8 Encoding**: Fixed international character corruption on Windows systems
  - Subprocess I/O now explicitly uses UTF-8 encoding instead of system default code page
  - Sets `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` environment variables for Windows
  - Properly encodes input as UTF-8 bytes and decodes output with error handling
  - Resolves issue #1 where Chinese and other non-ASCII characters were corrupted

### Added
- **Enhanced Windows CLI Detection**: Improved Codex CLI path detection on Windows
  - Added `.ps1` to supported Windows executable extensions
  - Added fallback checks for common Windows installation paths:
    - `%LOCALAPPDATA%\Programs\codex\codex.exe`
    - `%APPDATA%\npm\codex.cmd`
    - `%USERPROFILE%\.cargo\bin\codex.exe`
  - New `_build_codex_exec_command()` helper that uses the detected path
  - PowerShell scripts (.ps1) are now executed via `powershell -ExecutionPolicy Bypass -File`
- **Improved Error Diagnostics**: Better error messages for Windows users
  - Added `FileNotFoundError` specific handling with actionable guidance
  - Error responses now include platform information for debugging
  - Clear instructions to verify `codex --version` in Command Prompt

### Changed
- **Error Metadata**: All error responses now include `platform` and `exception_type` fields
- **Documentation**: Updated module docstring to mention Windows UTF-8 compatibility

## [1.2.2] - 2025-09-09

### Fixed
- **Windows Compatibility**: Added platform-specific subprocess handling for Windows
  - Removed `start_new_session=True` which is not supported on Windows
  - Added Windows executable detection (.exe, .bat, .cmd extensions)
  - Created `_run_codex_command()` helper for cross-platform execution

### Added
- **Platform Detection Utilities**: `_is_windows()` and `_get_codex_command()` functions
- **CI/CD Improvements**: Updated GitHub Actions for PyPI Trusted Publishing

## [1.2.1] - 2025-09-04

### Fixed
- **Error Handling Consistency**: Fixed invalid format parameter error handling to always return JSON
  - Previously returned plain text for invalid formats, now returns structured JSON error
  - Applied fix to both `consult_codex` and `consult_codex_with_stdin` functions
  - Ensures consistent API responses across all error conditions

### Added
- **Comprehensive Testing Suite**: New `tests/` directory with organized test structure
  - `tests/test_mcp_tools.py` - Complete test suite for all MCP tools functionality
  - `tests/README.md` - Testing documentation and guidelines
  - `tests/TEST_RESULTS.md` - Detailed test execution results and performance metrics
  - All tests passing with 100% functionality verification

### Changed
- **Code Quality**: Removed unused imports and resolved linting warnings
- **Project Structure**: Organized testing files in dedicated `tests/` directory
- **Documentation**: Enhanced testing documentation and contribution guidelines

### Tested
- ✅ All three MCP tools (`consult_codex`, `consult_codex_with_stdin`, `consult_codex_batch`)
- ✅ All output formats (text, JSON, code) with proper validation
- ✅ CODEX_SKIP_GIT_CHECK environment variable functionality  
- ✅ Error handling for invalid parameters and edge cases
- ✅ JSON response consistency and structure
- ✅ Code block extraction and processing

## [1.2.0] - 2025-01-03

### Added
- **Git Repository Check Configuration**: New `CODEX_SKIP_GIT_CHECK` environment variable
  - Allows running Codex Bridge in directories that are not Git repositories
  - Defaults to false for security; opt-in with "true", "1", or "yes"
  - Fixes "Not inside a trusted directory" errors when working outside Git repos
- **Enhanced Documentation**: Updated README.md and CLAUDE.md with new configuration options
- **Security Guidelines**: Added warnings about using git check bypass only in trusted directories

### Changed
- **Command Construction**: All three MCP tools now conditionally add `--skip-git-repo-check` flag
- **Error Handling**: Improved error messages and troubleshooting guidance

## [1.1.0] - 2025-01-28

### Changed
- **Default Format**: Changed default output format from "text" to "json" for structured responses
- **Default Timeout**: Increased default timeout from 60 to 90 seconds for better reliability
- **Documentation**: Updated function docstrings with timeout recommendations (60-120 seconds)
- **User Experience**: Improved out-of-the-box configuration to prevent hanging issues

### Added
- Enhanced timeout guidance in function documentation
- Better default configuration for production use

### Fixed
- Reduced likelihood of timeout-related hanging during complex queries
- Improved structured output consistency with JSON default

## [1.0.1] - 2025-01-28

### Fixed
- **Process Management**: Resolved infinite codex process spawning issue
- **CLI Integration**: Improved subprocess handling for better stability

### Changed
- **CI/CD**: Updated CI status badge URL to reflect new repository location
- **Build Process**: Removed deprecated activation scripts and configuration files

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