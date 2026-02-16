import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Testing key: {key[:10]}...") # Shows only the start for safety

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash')

try:
    response = model.generate_content("Hello")
    print("SUCCESS! The key works.")
    print(response.text)
except Exception as e:
    print(f"FAILED: {e}")