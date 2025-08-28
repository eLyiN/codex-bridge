# Contributing to Codex Bridge

Thank you for your interest in contributing to Codex Bridge! We welcome contributions from the community and are excited to work with you.

## 🚀 Getting Started

### Prerequisites

Before contributing, make sure you have:

- Python 3.9 or higher
- [Codex CLI](https://www.npmjs.com/package/@openai/codex-cli) installed and authenticated
- Git for version control
- A GitHub account

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/codex-bridge.git
   cd codex-bridge
   ```

3. **Set up the development environment**:
   ```bash
   # Install in development mode
   pip install -e .
   
   # Verify installation
   python -m src --help
   ```

4. **Verify Codex CLI is working**:
   ```bash
   codex --version
   codex auth login  # if not already authenticated
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔄 Development Workflow

### Making Changes

1. **Make your changes** in small, logical commits
2. **Test your changes** thoroughly:
   ```bash
   # Test the MCP server directly
   python -m src
   
   # Test integration with Claude Code (if available)
   ./start_server_dev.sh
   ```

3. **Follow code style guidelines** (see below)
4. **Update documentation** if needed

### Code Style Guidelines

- **Python**: Follow [PEP 8](https://pep8.org/) style guide
- **Line length**: Maximum 88 characters (Black formatter default)
- **Imports**: Group imports logically (standard library, third-party, local)
- **Docstrings**: Use clear, descriptive docstrings for functions and classes
- **Type hints**: Include type hints for function parameters and return values

### Example code style:
```python
from typing import Optional, List
import subprocess
import json

def consult_codex(
    query: str, 
    directory: str = ".", 
    format: str = "json",
    timeout: Optional[int] = None
) -> str:
    """
    Send a query to Codex CLI.
    
    Args:
        query: The question or prompt to send
        directory: Working directory for the query
        format: Output format - "text", "json", or "code" (default: "json")
        timeout: Optional timeout in seconds (recommended: 60-120)
        
    Returns:
        Codex's response as a formatted string
        
    Raises:
        RuntimeError: If CLI is not available or query fails
    """
    # Implementation here...
```

## 📝 Types of Contributions

We welcome several types of contributions:

### 🐛 Bug Fixes
- Fix existing bugs or issues
- Improve error handling
- Address edge cases

### ✨ Feature Enhancements
- Add new MCP tools (with justification)
- Improve existing tool functionality
- Add configuration options

### 📚 Documentation
- Improve README or other documentation
- Add usage examples
- Write tutorials or guides

### 🧪 Testing
- Add test cases
- Improve test coverage
- Add integration tests

### 🔧 Infrastructure
- Improve build process
- Update dependencies
- Enhance CI/CD

## 🔍 Pull Request Process

### Before Submitting

1. **Ensure your code works** with both development and production setups
2. **Write clear commit messages**:
   ```
   feat: add support for custom timeout configuration
   
   - Add timeout parameter to both MCP tools
   - Update documentation with timeout examples
   - Maintain backward compatibility with default 60s timeout
   ```

3. **Update relevant documentation**
4. **Test thoroughly** on your local setup

### Submitting Your PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - **Clear title** describing the change
   - **Detailed description** explaining:
     - What the change does
     - Why it's needed
     - How it was tested
     - Any breaking changes
   - **Link related issues** using `Fixes #123` or `Relates to #456`

### PR Review Process

1. **Automated checks** will run (when available)
2. **Maintainer review** will check:
   - Code quality and style
   - Functionality and correctness
   - Documentation updates
   - Backward compatibility
3. **Address feedback** promptly and professionally
4. **Final approval** and merge by maintainers

## 🚫 What We DON'T Accept

- Changes that add unnecessary complexity
- Features that duplicate existing functionality
- Breaking changes without strong justification and migration path
- Code that doesn't follow the project's simplicity philosophy
- Contributions without proper testing

## 🗣️ Communication Guidelines

### Reporting Issues

Use our [issue templates](.github/ISSUE_TEMPLATE/) for:
- **Bug reports**: Include reproduction steps, environment details
- **Feature requests**: Explain the use case and expected behavior
- **Questions**: Use GitHub Discussions for general questions

### Code Reviews

- **Be constructive** and respectful in feedback
- **Explain the "why"** behind suggestions
- **Learn from others** and be open to feedback
- **Focus on the code**, not the person

### Community Standards

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for community interaction guidelines.

## 📋 Testing Guidelines

### Manual Testing Checklist

Before submitting, verify:

- [ ] MCP server starts without errors
- [ ] `consult_codex` tool works with basic queries (defaults to JSON format)
- [ ] `consult_codex_with_stdin` tool works with stdin content
- [ ] `consult_codex_batch` tool works for batch processing
- [ ] Error handling works properly (try invalid queries)
- [ ] Timeout configuration works (test with CODEX_TIMEOUT environment variable)
- [ ] Documentation is updated and accurate

### Integration Testing

If possible, test with:
- Claude Code integration
- Different Python versions (3.9, 3.10, 3.11, 3.12)
- Various Codex models

## 🆘 Getting Help

### Questions and Support

- **GitHub Discussions**: For general questions and community discussion
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check existing docs first

### Maintainer Contact

For sensitive issues or maintainer-specific questions, you can reach out through:
- GitHub issues (preferred for transparency)
- Email (for security issues only)

## 📚 Resources

### Helpful Links

- [MCP (Model Context Protocol) Specification](https://modelcontextprotocol.io/)
- [Codex CLI Documentation](https://www.npmjs.com/package/@openai/codex-cli)
- [Python Packaging Guidelines](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

### Development Tools

Recommended tools for development:
- **Code Editor**: VS Code, PyCharm, or your preferred editor
- **Linting**: flake8, black, or ruff
- **Type Checking**: mypy
- **Git**: For version control

## 🙏 Recognition

Contributors are recognized in:
- GitHub contributor list
- CHANGELOG.md for significant contributions
- Special mentions for major features or fixes

Thank you for contributing to Codex Bridge! Your contributions help make this tool better for the entire community.

---

*This contributing guide is inspired by open source best practices and will evolve as our community grows.*