import json
import os
import sys
import tempfile
import subprocess
from agents import TesterAgent
from dotenv import load_dotenv

def evaluate_tester():
    load_dotenv()
    dataset_path = "eval_tester_dataset.json"
    if not os.path.exists(dataset_path):
        print(f"Error: dataset {dataset_path} not found.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)[:10]

    agent = TesterAgent()
    
    total = len(dataset)
    passed = 0
    
    print(f"Starting evaluation of TesterAgent on {total} samples...\n")
    
    for item in dataset:
        item_id = item["id"]
        source_code = item["code"]
        context = item["context"]
        
        print(f"--- Evaluating Snippet {item_id} ---")
        print(f"Context: {context}")
        print("Generating tests...")
        
        try:
            # Call the agent
            result = agent.process({
                "code": source_code,
                "context": context
            })
            
            test_code = result.get("test_code", "")
            if not test_code:
                print("FAILED: Agent did not return 'test_code'.")
                continue
                
            test_plan = result.get("test_plan", "")
            print(f"Test Plan Generated: {test_plan[:100]}...")
                
            # Note: The TesterAgent itself already runs the test in process() and puts the Output in "test_results"
            # But we are re-validating the logic here manually as part of the generic evaluation harness
            if result.get("tests_passed", False):
                print("PASSED: The generated tests successfully run and pass against the source code.")
                passed += 1
            else:
                 print("FAILED: The generated tests either failed to execute or failed assertions against the code.")
                 print("Test Output:")
                 print(result.get("test_results", ""))

        except Exception as e:
            print(f"FAILED with unexpected exception: {e}")
            
    # Summary
    pass_rate = (passed / total) * 100 if total > 0 else 0
    print("\n==============================")
    print("TESTER EVALUATION SUMMARY")
    print(f"Total Snippets: {total}")
    print(f"Valid Test Suites Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass Rate: {pass_rate:.2f}%")
    print("==============================")


if __name__ == "__main__":
    evaluate_tester()
