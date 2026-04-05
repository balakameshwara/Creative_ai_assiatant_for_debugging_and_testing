import os
from dotenv import load_dotenv
from agents import DebuggerAgent

load_dotenv()

def test_debugger_breakpoints():
    print("Testing DebuggerAgent for Breakpoint Suggestions...")
    
    agent = DebuggerAgent()
    
    sample_code = """
    def calculate_average(numbers):
        total = 0
        for n in numbers:
            total += n
        return total / 0  # Intentional error
    """
    
    sample_error = "ZeroDivisionError: division by zero"
    sample_context = "This function calculates the average of a list of numbers."
    
    input_data = {
        "code": sample_code,
        "error": sample_error,
        "context": sample_context
    }
    
    try:
        result = agent.process(input_data)
        print("\n--- Agent Response ---\n")
        print(result)
        print("\n----------------------\n")
        
        if "BREAKPOINT" in result.upper():
            print("SUCCESS: Breakpoint suggestions found in response.")
        else:
            print("WARNING: 'BREAKPOINT' keyword not clearly found in response. Please check output manually.")
            
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    test_debugger_breakpoints()
