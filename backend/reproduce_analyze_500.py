import os
from dotenv import load_dotenv
from agents import CodeIntegrityAgent
import traceback

# Load env vars
load_dotenv()

def test_integrity_agent():
    print("Initializing CodeIntegrityAgent...")
    agent = CodeIntegrityAgent()
    
    code_to_analyze = """
    def hello():
        print("Hello world")
    """
    
    print("Running process()...")
    try:
        result = agent.process({"code": code_to_analyze})
        print("Success!")
        print(result)
    except Exception:
        print("Caught exception:")
        traceback.print_exc()

if __name__ == "__main__":
    test_integrity_agent()
