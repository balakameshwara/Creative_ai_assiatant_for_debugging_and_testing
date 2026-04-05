
import os
import json
import traceback
from dotenv import load_dotenv
from agents import DebuggerAgent, TesterAgent, CodeIntegrityAgent

load_dotenv()

def validate_json_schema(data, schema_keys):
    if not isinstance(data, dict):
        return False, f"Expected dict, got {type(data).__name__}"
    missing = [key for key in schema_keys if key not in data]
    if missing:
        return False, f"Missing keys: {missing}"
    return True, "Valid"

def test_debugger_agent():
    print("\n[TEST] DebuggerAgent")
    agent = DebuggerAgent()
    code = "def foo():\n    return 1 / 0"
    error = "ZeroDivisionError: division by zero"
    context = ""
    
    print("  Running process...")
    try:
        result = agent.process({"code": code, "error": error, "context": context})
        print(f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        valid, msg = validate_json_schema(result, ["root_cause", "fixed_code", "breakpoints"])
        if valid:
            print("  [PASS] Structure valid.")
        else:
            print(f"  [FAIL] Structure invalid: {msg}")
            print(f"  Actual: {result}")
            
    except Exception as e:
        print(f"  [FAIL] Exception: {e}")
        traceback.print_exc()

def test_tester_agent():
    print("\n[TEST] TesterAgent")
    agent = TesterAgent()
    code = "def add(a, b): return a + b"
    context = ""
    
    print("  Running process...")
    try:
        result = agent.process({"code": code, "context": context})
        print(f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        valid, msg = validate_json_schema(result, ["test_plan", "test_code"])
        if valid:
            print("  [PASS] Structure valid.")
        else:
            print(f"  [FAIL] Structure invalid: {msg}")
            print(f"  Actual: {result}")

    except Exception as e:
        print(f"  [FAIL] Exception: {e}")
        traceback.print_exc()

def test_integrity_agent():
    print("\n[TEST] CodeIntegrityAgent")
    agent = CodeIntegrityAgent()
    code = "def terrible_function():\n    pass"
    
    print("  Running process...")
    try:
        result = agent.process({"code": code})
        print(f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        valid, msg = validate_json_schema(result, ["security_issues", "style_violations", "performance_suggestions", "refactoring_suggestions"])
        if valid:
            print("  [PASS] Structure valid.")
        else:
            print(f"  [FAIL] Structure invalid: {msg}")
            print(f"  Actual: {result}")

    except Exception as e:
        print(f"  [FAIL] Exception: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting Comprehensive Agent Verification...")
    test_debugger_agent()
    test_tester_agent()
    test_integrity_agent()
    print("\nDone.")
