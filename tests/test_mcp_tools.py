#!/usr/bin/env python3
"""
Test script for Codex Bridge MCP tools
Tests all three tools locally without uvx
"""

import json
import os
import sys
import pathlib

# Add parent directory to path for imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from src.mcp_server import consult_codex, consult_codex_with_stdin, consult_codex_batch

def test_basic_consult_codex():
    """Test basic consult_codex functionality"""
    print("🧪 Testing basic consult_codex...")
    
    # Test with text format
    result = consult_codex(
        query="What is 2+2?",
        directory="/Users/shelakh/mcp-servers/codex-bridge",
        format="text"
    )
    print("✅ Text format response received")
    print(f"Response length: {len(result)} characters")
    
    # Test with JSON format
    result_json = consult_codex(
        query="What is 2+2?",
        directory="/Users/shelakh/mcp-servers/codex-bridge", 
        format="json"
    )
    print("✅ JSON format response received")
    try:
        parsed = json.loads(result_json)
        print(f"✅ JSON is valid: {json.dumps(parsed, indent=2)}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print(f"Raw response: {result_json[:500]}...")
    
    print()

def test_code_format():
    """Test code format extraction"""
    print("🧪 Testing code format...")
    
    result = consult_codex(
        query="Write a Python function to calculate factorial",
        directory="/Users/shelakh/mcp-servers/codex-bridge",
        format="code"
    )
    
    try:
        parsed = json.loads(result)
        print("✅ Code format JSON is valid")
        code_blocks = parsed.get("code_blocks", [])
        print(f"✅ Found {len(code_blocks)} code blocks")
        for i, block in enumerate(code_blocks):
            print(f"  Block {i+1}: {block.get('language', 'unknown')} ({len(block.get('code', ''))} chars)")
    except json.JSONDecodeError as e:
        print(f"❌ Code format JSON parsing failed: {e}")
    
    print()

def test_stdin_functionality():
    """Test consult_codex_with_stdin"""
    print("🧪 Testing consult_codex_with_stdin...")
    
    test_code = """
def buggy_function(x):
    return x / 0  # This will cause ZeroDivisionError
"""
    
    result = consult_codex_with_stdin(
        stdin_content=test_code,
        prompt="What's wrong with this code and how can I fix it?",
        directory="/Users/shelakh/mcp-servers/codex-bridge",
        format="text"
    )
    
    print("✅ Stdin functionality working")
    print(f"Response length: {len(result)} characters")
    print(f"Contains 'zero': {'zero' in result.lower()}")
    print()

def test_batch_processing():
    """Test consult_codex_batch"""
    print("🧪 Testing consult_codex_batch...")
    
    queries = [
        {"query": "What is 1+1?", "timeout": 30},
        {"query": "What is 2*3?", "timeout": 30},
        {"query": "What is the capital of France?", "timeout": 30}
    ]
    
    result = consult_codex_batch(
        queries=queries,
        directory="/Users/shelakh/mcp-servers/codex-bridge"
    )
    
    try:
        parsed = json.loads(result)
        print("✅ Batch processing JSON is valid")
        print(f"✅ Status: {parsed.get('status')}")
        print(f"✅ Total queries: {parsed.get('total_queries')}")
        print(f"✅ Successful: {parsed.get('successful')}")
        print(f"✅ Failed: {parsed.get('failed')}")
        
        results = parsed.get('results', [])
        for i, res in enumerate(results):
            status = res.get('status', 'unknown')
            query = res.get('query', 'unknown')[:50] + '...'
            print(f"  Query {i+1}: {status} - {query}")
    except json.JSONDecodeError as e:
        print(f"❌ Batch processing JSON parsing failed: {e}")
    
    print()

def test_git_skip_check():
    """Test CODEX_SKIP_GIT_CHECK environment variable"""
    print("🧪 Testing CODEX_SKIP_GIT_CHECK functionality...")
    
    # Test in a non-git directory
    temp_dir = "/tmp/codex_test_dir"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Test without git skip (should fail in non-git dir)
    print("Testing without CODEX_SKIP_GIT_CHECK...")
    result1 = consult_codex(
        query="What is 1+1?",
        directory=temp_dir,
        format="text",
        timeout=15
    )
    
    if "error" in result1.lower() or "git" in result1.lower():
        print("✅ Git check working as expected (failed in non-git dir)")
    else:
        print("⚠️  Expected git error, but query succeeded")
    
    # Test with git skip enabled
    print("Testing with CODEX_SKIP_GIT_CHECK=true...")
    os.environ["CODEX_SKIP_GIT_CHECK"] = "true"
    
    result2 = consult_codex(
        query="What is 1+1?", 
        directory=temp_dir,
        format="text",
        timeout=15
    )
    
    if "error" not in result2.lower():
        print("✅ Git skip check working (succeeded in non-git dir)")
    else:
        print(f"❌ Git skip failed: {result2}")
    
    # Cleanup
    os.environ.pop("CODEX_SKIP_GIT_CHECK", None)
    print()

def test_error_handling():
    """Test error handling"""
    print("🧪 Testing error handling...")
    
    # Test invalid directory
    result = consult_codex(
        query="test",
        directory="/nonexistent/directory",
        format="json"
    )
    
    try:
        parsed = json.loads(result)
        if parsed.get("status") == "error":
            print("✅ Invalid directory error handled correctly")
        else:
            print("❌ Expected error status for invalid directory")
    except json.JSONDecodeError:
        print("❌ Error response not in valid JSON format")
    
    # Test invalid format
    result = consult_codex(
        query="test",
        directory="/Users/shelakh/mcp-servers/codex-bridge",
        format="invalid_format"
    )
    
    try:
        parsed = json.loads(result)
        if parsed.get("status") == "error":
            print("✅ Invalid format error handled correctly")
        else:
            print("❌ Expected error status for invalid format")
    except json.JSONDecodeError:
        print("❌ Error response not in valid JSON format")
    
    print()

def main():
    """Run all tests"""
    print("🚀 Starting Codex Bridge MCP Tools Test Suite")
    print("=" * 50)
    
    test_basic_consult_codex()
    test_code_format()
    test_stdin_functionality()
    test_batch_processing()
    test_git_skip_check()
    test_error_handling()
    
    print("🎉 Test suite completed!")

if __name__ == "__main__":
    main()