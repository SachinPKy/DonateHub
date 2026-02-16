import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load environment
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env', override=True)

# Test Gemini API directly
from google.genai import Client

api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing Gemini API with new SDK...")
print(f"API Key: {api_key[:30]}...")

try:
    client = Client(api_key=api_key)
    
    prompt = (
        "Choose ONE category from this list ONLY:\n"
        "Clothes, Books, Toys, Electronics, Furniture, Footwear, "
        "Educational Materials, Household Items.\n\n"
        f"Description: torch\n"
        "Return only the category name."
    )
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    category = response.text.lower()
    
    print("✅ SUCCESS! Gemini API works!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)
