
import os

import re
from dotenv import load_dotenv
from agents import TesterAgent

load_dotenv()

def extract_code_block(text):
    """Extracts python code from markdown code blocks"""
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def verify_generated_tests():
    print("Generating tests for 'Simple Pure Function'...")
    
    code_to_test = """
def add(a, b):
    return a + b
"""
    
    agent = TesterAgent()
    result = agent.process({"code": code_to_test})
    
    extracted_test_code = extract_code_block(result)
    
    # Create a standalone test file
    test_file_content = f"""
import unittest

# --- Target Code ---
{code_to_test}
# -------------------

# --- Generated Tests ---
{extracted_test_code}
# -----------------------

if __name__ == '__main__':
    unittest.main()
"""
    
    with open("temp_generated_tests.py", "w") as f:
        f.write(test_file_content)
        
    print("Saved generated tests to 'temp_generated_tests.py'.")
    print("You can now run 'python temp_generated_tests.py' to verify them.")

if __name__ == "__main__":
    verify_generated_tests()
