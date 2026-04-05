import os
import sys
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from agents import DebuggerAgent
import pytest

# Mocking external dependencies
sys.modules["langchain_google_genai"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["langchain_core.output_parsers"] = MagicMock()

def test_debugger_agent_exhaustion():
    print("Testing DebuggerAgent fallback exhaustion...")
    
    # Create the agent
    agent = DebuggerAgent()
    
    # Mock the LLM chain to always raise an exception with "RESOURCE_EXHAUSTED"
    # We need to patch _run_with_retry or the chain invocation itself.
    # Since _run_with_fallback creates the chain, let's patch ChatGoogleGenerativeAI to return a mock
    # that raises an error when invoked.
    
    with patch("agents.ChatGoogleGenerativeAI") as MockLLM:
        mock_instance = MockLLM.return_value
        # We need to mock the chain behavior.
        # In _run_with_fallback: chain = prompt_template | llm | StrOutputParser()
        # This is hard to mock essentially because of the pipe operator overriding.
        
        # A easier way might be to patch _run_with_retry which is called by _run_with_fallback
        # But we want to test _run_with_fallback's logic mostly.
        
        # Let's try patching _run_with_retry to simulate failure
        with patch.object(
            agent, 
            "_run_with_retry", 
            side_effect=Exception("429 RESOURCE_EXHAUSTED")
        ):
            try:
                agent.process({"code": "print('hello')", "error": "test error", "context": ""})
            except Exception as e:
                print(f"Caught expected exception: {e}")
                print(f"Exception type: {type(e)}")
                # Check if this exception would be caught by server.py handler
                # server.py checks: if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                error_str = str(e)
                if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                    print("PASS: Exception contains rate limit keywords.")
                else:
                    print("FAIL: Exception DOES NOT contain rate limit keywords.")
                    print(f"String representation: '{error_str}'")

if __name__ == "__main__":
    test_debugger_agent_exhaustion()
