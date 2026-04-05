import requests
import time

def test_analyze():
    print("Sending request to /analyze...")
    try:
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"code": "def hello():\n    print('hello world')"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_analyze()
