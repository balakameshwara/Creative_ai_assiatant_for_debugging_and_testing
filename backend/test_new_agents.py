
import os
import sys
from dotenv import load_dotenv

# Ensure backend is in path
sys.path.append(os.path.join(os.getcwd()))

from agents import FileEditorAgent, MultiFileAnalysisAgent

load_dotenv()

def test_file_editor():
    print("\n--- Testing FileEditorAgent ---")
    agent = FileEditorAgent()
    
    code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""
    instruction = "Rename the function to 'calc_cart_total' and add a type hint to the return value (float)."
    
    print(f"Instruction: {instruction}")
    try:
        result = agent.process({"code": code, "instruction": instruction})
        print("Result:")
        print(result)
        
        if "def calc_cart_total" in result and "-> float" in result:
            print("SUCCESS: File Editor modifications verified.")
        else:
            print("FAILURE: output did not match expectation.")
            
    except Exception as e:
        print(f"Error: {e}")

def test_multi_file_analysis():
    print("\n--- Testing MultiFileAnalysisAgent ---")
    agent = MultiFileAnalysisAgent()
    
    files = {
        "api.py": """
from db import get_user

def login(username, password):
    user = get_user(username)
    if user.password == password:
        return True
    return False
""",
        "db.py": """
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def get_user(username):
    # Mock database lookup
    return User(username, "secret")
"""
    }
    
    question = "How does api.py interact with db.py? What function is called?"
    
    print(f"Question: {question}")
    try:
        result = agent.process({"files": files, "question": question})
        print("Result:")
        print(result)
        
        if "get_user" in result:
            print("SUCCESS: Multi-file relationship identified.")
        else:
            print("FAILURE: 'get_user' not found in analysis.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_file_editor()
    test_multi_file_analysis()
