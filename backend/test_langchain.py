from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing LangChain Gemini Integration...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

try:
    print("Sending request...")
    result = llm.invoke("Hello, are you working?")
    print("Success!")
    print(result.content)
except Exception as e:
    print("Failed!")
    print(e)
