from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import CodeSubmission
from .forms import CodeSubmissionForm
from .compiler import CodeCompiler
import json

def compiler_view(request):
    """Main compiler page view"""
    form = CodeSubmissionForm()
    recent_submissions = CodeSubmission.objects.all().order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_submissions': recent_submissions
    }
    return render(request, 'compiler/compiler.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def run_code(request):
    """API endpoint to run code"""
    try:
        data = json.loads(request.body)
        language = data.get('language', 'python')
        code = data.get('code', '')
        input_data = data.get('input_data', '')
        
        if not code.strip():
            return JsonResponse({
                'success': False,
                'error': 'Code cannot be empty'
            })
        
        # Initialize compiler
        compiler = CodeCompiler()
        
        # Compile and run the code
        result = compiler.compile_and_run(code, language, input_data)
        
        # Save submission to database
        submission = CodeSubmission.objects.create(
            user=request.user if request.user.is_authenticated else None,
            language=language,
            code=code,
            input_data=input_data,
            output=result.get('output', ''),
            error_message=result.get('error', ''),
            execution_time=result.get('execution_time', 0),
            status=result.get('status', 'error')
        )
        
        # Clean up
        compiler.cleanup()
        
        return JsonResponse({
            'success': True,
            'submission_id': submission.unique_id,
            'output': result.get('output', ''),
            'error': result.get('error', ''),
            'execution_time': result.get('execution_time', 0),
            'status': result.get('status', 'error')
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

def submission_detail(request, submission_id):
    """View to show details of a specific submission"""
    submission = get_object_or_404(CodeSubmission, unique_id=submission_id)
    return render(request, 'compiler/submission_detail.html', {'submission': submission})

@login_required
def my_submissions(request):
    """View to show user's own submissions"""
    submissions = CodeSubmission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'compiler/my_submissions.html', {'submissions': submissions}) 