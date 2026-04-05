import requests

print("Testing Backend Analysis Endpoint...")
try:
    response = requests.post(
        "http://localhost:8000/analyze",
        json={"code": "def hello():\n    print('hello')\n"}
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print("Failed!")
        print(response.text)
except Exception as e:
    print(f"Connection Error: {e}")
