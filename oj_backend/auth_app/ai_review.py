import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

@csrf_exempt
def ai_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            language = data.get("language", "python")

            prompt = f"Review the following {language} code. Give suggestions, point out bugs, and recommend improvements:\n\n{code}"

            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            params = {"key": GEMINI_API_KEY}
            headers = {"Content-Type": "application/json"}

            response = requests.post(GEMINI_API_URL, params=params, headers=headers, json=payload)
            ai_reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response.")

            return JsonResponse({"review": ai_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
