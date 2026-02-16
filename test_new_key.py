import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Testing key: {key[:20]}...")

try:
    client = Client(api_key=key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents="Hello")
    print("SUCCESS! The key works with google-genai SDK.")
    print(f"Response: {response.text[:100]}")
except Exception as e:
    print(f"FAILED: {e}")
