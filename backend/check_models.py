import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    try:
        genai.configure(api_key=api_key)
        print("Successfully configured with API key.")
        print("Listing available models:")
        for m in genai.list_models():
            if 'embedContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
