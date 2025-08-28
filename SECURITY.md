# Security Policy

## Supported Versions

We provide security updates for the following versions of Codex Bridge:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them by:

1. **Email**: Send details to the maintainer via GitHub (preferred)
2. **GitHub Security**: Use GitHub's private vulnerability reporting feature
3. **Direct Contact**: Create a private issue if the above options aren't available

### What to Include

When reporting a vulnerability, please provide:

- **Description**: Clear description of the vulnerability
- **Impact**: What could an attacker accomplish?
- **Reproduction**: Step-by-step instructions to reproduce the issue
- **Environment**: Python version, OS, Codex CLI version
- **Suggested Fix**: If you have ideas for a solution

### Example Report Template

```
**Vulnerability Type**: [e.g., Code Injection, Information Disclosure]
**Severity**: [Low/Medium/High/Critical]
**Affected Component**: [e.g., consult_codex function, file handling]

**Description**:
[Detailed description of the vulnerability]

**Steps to Reproduce**:
1. [Step one]
2. [Step two]
3. [Step three]

**Impact**:
[What could happen if this is exploited]

**Environment**:
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.5]
- Codex CLI: [e.g., 1.2.3]
- Codex Bridge: [e.g., 1.0.0]
```

## Response Timeline

We aim to respond to security reports according to this timeline:

- **Acknowledgment**: Within 48 hours of report
- **Initial Assessment**: Within 1 week
- **Status Update**: Weekly updates on progress
- **Resolution**: Depends on severity and complexity

### Severity Levels

- **Critical**: Immediate threat, affects all users
- **High**: Significant threat, affects many users
- **Medium**: Moderate threat, limited impact
- **Low**: Minor threat, minimal impact

## Security Best Practices

### For Users

When using Codex Bridge:

1. **Keep Updated**: Always use the latest version
2. **Secure Authentication**: Protect your Codex CLI authentication
3. **File Permissions**: Be careful with file paths and permissions
4. **Network Security**: Use secure networks when possible
5. **Input Validation**: Be cautious with untrusted input in queries

### For Developers

When contributing to Codex Bridge:

1. **Input Sanitization**: Always validate and sanitize user input
2. **Path Traversal**: Prevent directory traversal attacks
3. **Command Injection**: Avoid shell injection vulnerabilities
4. **Error Information**: Don't leak sensitive info in error messages
5. **Dependencies**: Keep dependencies updated and secure

## Known Security Considerations

### Current Architecture

- **CLI Dependency**: Security depends on Codex CLI installation
- **File Access**: MCP tools can access files in specified directories
- **Subprocess Calls**: Uses subprocess to call Codex CLI
- **Network Requests**: Codex CLI makes network requests to OpenAI

### Mitigation Strategies

- **Timeout Protection**: 60-second timeout prevents long-running attacks
- **Error Handling**: Graceful error handling without information leakage
- **No Persistent State**: Stateless operation reduces attack surface
- **Simple Architecture**: Minimal code reduces potential vulnerabilities

## Security Updates

### How We Handle Security Issues

1. **Assessment**: Evaluate the severity and impact
2. **Fix Development**: Develop and test a security fix
3. **Coordinated Disclosure**: Work with reporter on disclosure timeline
4. **Release**: Deploy security update as patch release
5. **Notification**: Notify users through appropriate channels

### Update Notifications

Security updates are announced through:

- **GitHub Releases**: All releases include security notes
- **GitHub Security Advisories**: For significant vulnerabilities
- **README Updates**: Security-related changes noted
- **CHANGELOG**: Detailed security fix information

## Disclosure Policy

### Responsible Disclosure

We follow responsible disclosure practices:

- **Private Reporting**: Initial reports should be private
- **Coordinated Timeline**: Work together on disclosure timing
- **Credit**: Security researchers receive appropriate credit
- **Public Disclosure**: After fix is available and deployed

### Timeline Example

1. **Day 0**: Vulnerability reported privately
2. **Day 1-2**: Acknowledgment and initial assessment
3. **Day 3-14**: Fix development and testing
4. **Day 14-21**: Security update release
5. **Day 21+**: Public disclosure (if appropriate)

## Security-Related Dependencies

### Direct Dependencies

- **mcp**: Model Context Protocol library
  - Keep updated to latest stable version
  - Monitor for security advisories

### External Dependencies

- **Codex CLI**: OpenAI's official CLI tool
  - Security managed by Google
  - Users should keep updated
  - Authentication handled by Google

### System Dependencies

- **Python**: Use supported Python versions (3.9+)
- **Operating System**: Keep OS updated for subprocess security
- **Network**: Secure network configuration recommended

## Security Questions

For general security questions (non-vulnerabilities):

- Check existing documentation first
- Use GitHub Discussions for community input
- Create GitHub issues for documentation improvements
- Email maintainers for sensitive questions

## Acknowledgments

We thank the security research community for helping keep Codex Bridge secure:

- [Future security researchers will be listed here]

## Resources

### Security Tools and Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guidelines](https://python.org/dev/security/)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [MCP Security Considerations](https://modelcontextprotocol.io/)

---

**Remember**: When in doubt about security, it's better to report a false positive than to ignore a potential vulnerability.