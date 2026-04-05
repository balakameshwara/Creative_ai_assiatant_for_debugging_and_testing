import os
import json
from dotenv import load_dotenv
from agents import TesterAgent

# Load environment variables
load_dotenv()

def run_test_case(name, code, context=""):
    print(f"\n{'='*50}")
    print(f"Running Test Case: {name}")
    print(f"{'='*50}")
    print(f"Input Code:\n{code.strip()}\n")
    
    agent = TesterAgent()
    input_data = {
        "code": code,
        "context": context
    }
    
    try:
        # The agent returns a dictionary (JSON input)
        result = agent.process(input_data)
        
        # Check if result is a dict (parsed JSON)
        if isinstance(result, dict):
            print("--- Agent Generated Test Plan ---")
            print(result.get("test_plan", "No plan returned"))
            print("\n--- Agent Generated Test Code ---")
            print(result.get("test_code", "No code returned"))
            
            if "test_results" in result:
                print("\n--- Test Execution Results ---")
                status = "PASSED" if result.get("tests_passed") else "FAILED"
                print(f"Status: {status}")
                print(result["test_results"])
                
            if "error" in result:
                 print(f"\nERROR: {result['error']}")
                 print(f"Raw Response: {result.get('raw_response', '')}")
        else:
            print("--- Agent Result (Unexpected Type) ---")
            print(result)

        print("-----------------------------")
        return True
    except Exception as e:
        print(f"ERROR: Agent failed to process request: {e}")
        return False

if __name__ == "__main__":
    print("Starting TesterAgent Verification...")

    # Case 1: Simple Pure Function
    code_1 = """
def add(a, b):
    return a + b
"""
    run_test_case("Simple Pure Function", code_1)

    # Case 2: Boundary Conditions
    code_2 = """
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
"""
    run_test_case("Boundary Conditions", code_2)

    # Case 3: Exception Handling
    code_3 = """
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""
    run_test_case("Exception Handling", code_3)

    # Case 4: String Manipulation
    code_4 = """
def is_palindrome(s):
    clean_s = ''.join(c.lower() for c in s if c.isalnum())
    return clean_s == clean_s[::-1]
"""
    run_test_case("String Manipulation", code_4)
    
    print("\nVerification Complete.")
