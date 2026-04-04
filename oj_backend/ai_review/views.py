import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from judge.models import Problem

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print(" Critical Error: Could not import google.generativeai (ImportError)")

# Configure Gemini API with better environment variable handling
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("  WARNING: GEMINI_API_KEY environment variable not set.")
    print("  AI Review functionality will be disabled.")
    GEMINI_API_KEY = None
else:
    print(f" API Key loaded: {GEMINI_API_KEY[:10]}...")

# Only configure Gemini if API key is available
if GEMINI_API_KEY and genai:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print(" Gemini API configured successfully")
    except Exception as e:
        print(f" Error configuring Gemini API: {e}")
        GEMINI_API_KEY = None
else:
    print(" Gemini API not configured - AI Review disabled")


@csrf_exempt
@login_required
def ai_review(request):
    """AI Review endpoint for code analysis using Gemini"""
    if request.method == 'POST':
        try:
            # Check if API key is available
            if not GEMINI_API_KEY:
                return JsonResponse({
                    'error': 'AI Review is currently disabled. Please contact the administrator to enable this feature.',
                    'details': 'GEMINI_API_KEY environment variable not set'
                }, status=503)

            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            problem_id = data.get('problem_id')

            if not code.strip():
                return JsonResponse({'error': 'No code provided'}, status=400)

            # Get problem details if available
            problem_context = ""
            if problem_id:
                try:
                    problem = Problem.objects.get(id=problem_id)
                    problem_context = f"""
                    Problem: {problem.title}
                    Description: {problem.description}
                    Difficulty: {problem.difficulty}
                    """
                except Problem.DoesNotExist:
                    pass

            # Create a structured prompt for Gemini
            prompt = f"""
            You are an expert programming mentor and code reviewer. Analyze the following {language} code and provide a comprehensive, structured review with specific code suggestions.

            {problem_context}

            Code to review:
            ```{language}
            {code}
            ```

            Please provide a structured review covering:

            1. **Code Quality Assessment** (1-2 sentences)
            2. **Algorithm Analysis** (1-2 sentences)
            3. **Time & Space Complexity** (if applicable)
            4. **Potential Issues** (if any)
            5. **Code Improvement Suggestions** (Provide specific code snippets with improvements)
            6. **Overall Rating** (Good/Fair/Needs Improvement)

            For the "Code Improvement Suggestions" section:
            - If the code is already well-written, acknowledge that
            - If there are improvements needed, provide specific code snippets showing the suggested changes
            - Use markdown code blocks with the language specified
            - Explain why each suggestion improves the code
            - Focus on readability, efficiency, and best practices

            Keep each section concise and actionable. Format your response with bold headers and clear code examples.
            """

            # Generate response using Gemini
            try:
                model = genai.GenerativeModel('gemini-3.0-pro')
                response = model.generate_content(prompt)
            except Exception as e:
                try:
                    model = genai.GenerativeModel('gemini-3.0-flash')
                    response = model.generate_content(prompt)
                except Exception as e2:
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content(prompt)
                    except Exception as e3:
                        return JsonResponse({
                            'error': 'AI Review service is temporarily unavailable. Please try again later.',
                            'details': f'All Gemini models failed: {str(e3)}'
                        }, status=503)

            # Extract the response text
            if hasattr(response, 'text') and response.text:
                review_text = response.text
            else:
                review_text = "Unable to generate review at this time."

            print(f" AI Review generated successfully")

            return JsonResponse({
                'success': True,
                'review': review_text,
                'language': language
            })

        except Exception as e:
            return JsonResponse({
                'error': f'AI Review failed: {str(e)}'
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
