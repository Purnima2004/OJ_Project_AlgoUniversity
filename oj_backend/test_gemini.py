#!/usr/bin/env python3
"""
Test script to check available Gemini models
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-api-key-here')
genai.configure(api_key=GOOGLE_API_KEY)

print(f"API Key loaded: {GOOGLE_API_KEY[:10]}...")

# List available models
print("\n🔍 Checking available models...")
try:
    models = genai.list_models()
    print("Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✅ {model.name} - {model.display_name}")
        else:
            print(f"  ❌ {model.name} - {model.display_name} (no generateContent)")
except Exception as e:
    print(f"Error listing models: {e}")

# Test different model names
test_models = [
    'gemini-1.5-pro',
    'gemini-1.5-flash', 
    'gemini-pro',
    'gemini-pro-vision'
]

print("\n🧪 Testing model access...")
for model_name in test_models:
    try:
        model = genai.GenerativeModel(model_name)
        print(f"  ✅ {model_name} - Accessible")
        
        # Try a simple test
        response = model.generate_content("Say 'Hello World'")
        if hasattr(response, 'text'):
            print(f"Response: {response.text[:50]}...")
        else:
            print(f"No text response")
            
    except Exception as e:
        print(f"  ❌ {model_name} - Error: {str(e)[:100]}...")

print("\n✅ Test completed!") 