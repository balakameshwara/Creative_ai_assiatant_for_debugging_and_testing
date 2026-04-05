import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_analyze():
    print("Testing /analyze endpoint...")
    payload = {
        "code": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)"
    }
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        if response.status_code == 200:
            print("[PASS] /analyze returned 200 OK")
            print("Response:", response.json())
        else:
            print(f"[FAIL] /analyze returned {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[ERROR] /analyze failed: {e}")

def test_debug():
    print("\nTesting /debug endpoint...")
    payload = {
        "code": "def add(a, b):\n    return a + b",
        "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    }
    try:
        response = requests.post(f"{BASE_URL}/debug", json=payload)
        if response.status_code == 200:
            print("[PASS] /debug returned 200 OK")
            print("Response:", response.json())
        else:
            print(f"[FAIL] /debug returned {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[ERROR] /debug failed: {e}")

if __name__ == "__main__":
    print("Waiting for server to be ready...")
    # Simple check to see if server is up
    try:
        requests.get(f"{BASE_URL}/")
        print("Server is up.")
    except:
        print("Server seems down. Please ensure it is running.")
        exit(1)
        
    test_analyze()
    time.sleep(1) # Be nice
    test_debug()
