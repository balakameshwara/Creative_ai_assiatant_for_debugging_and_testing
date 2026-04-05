import json
import os
import sys
import tempfile
import subprocess
from agents import DebuggerAgent
from dotenv import load_dotenv

def evaluate_debugger():
    load_dotenv()
    dataset_path = "eval_dataset_multilang.json"
    if not os.path.exists(dataset_path):
        print(f"Error: dataset {dataset_path} not found.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)[:50]

    agent = DebuggerAgent()
    
    total = len(dataset)
    passed = 0
    
    print(f"Starting evaluation of DebuggerAgent on {total} samples...\n")
    
    for item in dataset:
        item_id = item["id"]
        buggy_code = item["buggy_code"]
        error_message = item["error_message"]
        expected_behavior = item["expected_behavior"]
        test_code = item["unit_test"]
        
        print(f"--- Evaluating Snippet {item_id} ---")
        print(f"Error: {error_message}")
        print("Generating fix...")
        
        try:
            # Call the agent
            result = agent.process({
                "code": buggy_code,
                "error": error_message,
                "context": expected_behavior
            })
            
            fixed_code = result.get("fixed_code", "")
            if not fixed_code:
                print("FAILED: Agent did not return 'fixed_code'.")
                continue
                
            # Clean up markdown code blocks if the agent included them
            fixed_code = fixed_code.strip()
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code[9:]
            elif fixed_code.startswith("```"):
                fixed_code = fixed_code[3:]
            if fixed_code.endswith("```"):
                fixed_code = fixed_code[:-3]
            fixed_code = fixed_code.strip()
                
            # Verify the fix
            with tempfile.TemporaryDirectory() as temp_dir:
                target_file = os.path.join(temp_dir, "target_module.py")
                test_file = os.path.join(temp_dir, "test_target.py")
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                    
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(test_code)
                    
                # Run pytest
                process = subprocess.run(
                    [sys.executable, "-m", "pytest", "test_target.py"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                # Check results
                if process.returncode == 0:
                    print("PASSED: The generated fix successfully passed the unit tests.")
                    passed += 1
                else:
                    # In some environments pytest might not be available, fallback to unittest check
                    if "No module named pytest" in process.stderr:
                        process = subprocess.run(
                            [sys.executable, "-m", "unittest", "test_target.py"],
                            cwd=temp_dir,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if process.returncode == 0:
                            print("PASSED: The generated fix successfully passed the unit tests.")
                            passed += 1
                            import time
                            time.sleep(30)  # 15 RPM limit avoidance (4s + generation time > 4s = ~10-15 RPM max)
                            continue
                            
                    print("FAILED: The generated fix did not pass the unit tests.")
                    print("Test Output:")
                    print(process.stdout)
                    if process.stderr:
                        print(process.stderr)
                    
        except Exception as e:
            print(f"FAILED with unexpected exception: {e}")
            
        import time
        time.sleep(30)  # 15 RPM limit avoidance
            
    # Summary
    pass_rate = (passed / total) * 100 if total > 0 else 0
    print("\n==============================")
    print("EVALUATION SUMMARY")
    print(f"Total Snippets: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass Rate: {pass_rate:.2f}%")
    print("==============================")

if __name__ == "__main__":
    evaluate_debugger()
