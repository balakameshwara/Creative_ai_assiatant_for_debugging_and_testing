from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    print("Attempting to invoke model...")
    response = llm.invoke("Hello, are you working?")
    print("Response received:")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")
