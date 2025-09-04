# Codex Bridge Testing Suite

This directory contains comprehensive tests for the Codex Bridge MCP server.

## 📁 Test Structure

```
tests/
├── README.md                # This file - testing overview
├── test_mcp_tools.py        # Main test suite for all MCP tools
├── TEST_RESULTS.md          # Latest test execution results
└── test_reports/            # Historical test reports (future)
```

## 🧪 Running Tests

### Prerequisites
- Codex CLI installed and authenticated (`codex --version`)
- Python 3.10+ with MCP server dependencies
- Local development environment set up

### Quick Test
```bash
# Run from project root
python tests/test_mcp_tools.py
```

### Individual Test Functions
```python
# Import specific tests if needed
from tests.test_mcp_tools import test_basic_consult_codex, test_git_skip_check

# Run individual tests
test_basic_consult_codex()
test_git_skip_check()
```

## 🔍 Test Categories

### 1. Core Functionality Tests
- **Basic consult_codex:** Text and JSON format responses
- **Code format:** Code block extraction and formatting
- **Stdin processing:** Pipeline-friendly content processing
- **Batch processing:** Multiple query handling

### 2. Environment & Configuration Tests
- **CODEX_SKIP_GIT_CHECK:** Git repository bypass functionality
- **Timeout handling:** Custom timeout configuration
- **Directory validation:** Path security checks

### 3. Error Handling Tests
- **Invalid parameters:** Format validation, directory checks
- **CLI availability:** Codex CLI detection
- **JSON consistency:** Structured error responses

## 📊 Test Results Interpretation

### Success Indicators
- ✅ **Green checkmarks:** Test passed
- **Response lengths:** Typical 300-5000 characters
- **JSON validity:** All JSON responses parse correctly
- **Code block detection:** 1-7 blocks found per query

### Failure Indicators
- ❌ **Red X marks:** Test failed
- **Error messages:** Specific failure reasons
- **JSON parsing errors:** Invalid response format

## 🔧 Troubleshooting Tests

### Common Issues
1. **"CLI not available"**
   - Install: `npm install -g @openai/codex-cli`
   - Authenticate: `codex auth login`

2. **"Git repository" errors**
   - Normal behavior in non-git directories
   - Use `CODEX_SKIP_GIT_CHECK=true` if needed

3. **Timeout errors**
   - Increase timeout: `CODEX_TIMEOUT=120`
   - Check network connectivity

### Debug Mode
```python
# Add debug prints to test functions
def test_basic_consult_codex():
    print("🐛 Debug: Starting basic test...")
    result = consult_codex(query="test", directory=".", format="json")
    print(f"🐛 Debug: Raw result: {result[:200]}...")
```

## 📝 Adding New Tests

### Test Function Template
```python
def test_new_feature():
    """Test description"""
    print("🧪 Testing new feature...")
    
    # Setup
    test_input = "example input"
    
    # Execute
    result = consult_codex(
        query=test_input,
        directory="/path/to/test/dir",
        format="json"
    )
    
    # Validate
    try:
        parsed = json.loads(result)
        if parsed.get("status") == "success":
            print("✅ New feature test passed")
        else:
            print("❌ New feature test failed")
    except json.JSONDecodeError:
        print("❌ New feature returned invalid JSON")
    
    print()
```

### Test Checklist
- [ ] Clear test description and purpose
- [ ] Proper setup and cleanup
- [ ] Multiple test cases (success/error)
- [ ] JSON validation where applicable
- [ ] Clear success/failure indicators
- [ ] Integration with main test suite

## 📋 Test Maintenance

### Regular Testing
- Run full suite before releases
- Test after environment changes
- Validate after dependency updates

### Test Data Management
- Keep test queries simple and reliable
- Use deterministic test inputs when possible
- Document expected response patterns

### CI/CD Integration (Future)
```yaml
# Example GitHub Actions test step
- name: Run MCP Tools Tests
  run: python tests/test_mcp_tools.py
  env:
    CODEX_TIMEOUT: 120
    CODEX_SKIP_GIT_CHECK: true
```

## 🚀 Performance Testing

### Response Time Benchmarks
- Basic queries: 4-15 seconds
- Code generation: 10-20 seconds
- File analysis: 15-30 seconds
- Batch processing: 30-60 seconds

### Load Testing (Future)
- Multiple concurrent requests
- Memory usage monitoring
- Timeout behavior under load

## 📊 Test Coverage

### Current Coverage
- ✅ All three MCP tools tested
- ✅ All output formats (text, json, code)
- ✅ Error conditions covered
- ✅ Environment variables tested
- ✅ Git repository checks validated

### Future Coverage Goals
- Integration tests with real MCP clients
- Performance regression testing
- Cross-platform compatibility tests
- Extended timeout scenarios

---

For questions about testing, see [CONTRIBUTING.md](../CONTRIBUTING.md) or open an issue on GitHub.