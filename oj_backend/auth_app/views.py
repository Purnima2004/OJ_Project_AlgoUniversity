from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Problem, Contest, UserProfile, Submission, ConceptOfDay, CodeSubmission
from .forms import CodeSubmissionForm
from .compiler import CodeCompiler
import json

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        except IntegrityError:
            return render(request, 'register/register.html', {
                'error': 'Username already exists. Please choose a different username.'
            })
    return render(request, 'register/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'login/login.html', {
                'error': 'Please provide both username and password.'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login/login.html', {
                'error': 'Invalid username or password. Please try again.'
            })
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    contests = Contest.objects.all()[:3]
    concept_of_day = ConceptOfDay.objects.first()
    
    if not concept_of_day:
        concept_of_day = {
            'title': 'Dynamic Programming',
            'description': 'Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. It is applicable when the subproblems are not independent, that is, when subproblems share subsubproblems.',
            'example_code': 'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)'
        }
    
    context = {
        'contests': contests,
        'concept_of_day': concept_of_day,
        'total_problems': Problem.objects.count(),
        'total_users': User.objects.count(),
        'total_submissions': Submission.objects.count(),
    }
    return render(request, 'home/home.html', context)

def problems_view(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problems.html', {'problems': problems})

def contests_view(request):
    contests = Contest.objects.all()
    return render(request, 'contests/contests.html', {'contests': contests})

def submissions_view(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    else:
        submissions = []
    return render(request, 'submission/submissions.html', {'submissions': submissions})

def leaderboard_view(request):
    user_profiles = UserProfile.objects.all().order_by('-score')
    return render(request, 'leaderboard/leaderboard.html', {'user_profiles': user_profiles})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    
    # Hardcoded problems for demo
    if problem_id == 1:
        problem.examples = [
            {'input': '5', 'output': '120', 'explanation': '5! = 5 × 4 × 3 × 2 × 1 = 120'},
            {'input': '0', 'output': '1', 'explanation': '0! = 1 by definition'},
            {'input': '3', 'output': '6', 'explanation': '3! = 3 × 2 × 1 = 6'}
        ]
        problem.constraints = ['0 ≤ n ≤ 12', 'The result fits in a 32-bit integer']
        problem.test_cases = [
            {'input': '5', 'expected_output': '120'},
            {'input': '0', 'expected_output': '1'},
            {'input': '3', 'expected_output': '6'},
            {'input': '10', 'expected_output': '3628800'}
        ]
    elif problem_id == 2:
        problem.examples = [
            {'input': '[1,2,3,4,5]', 'output': '15', 'explanation': 'Sum of all elements: 1+2+3+4+5 = 15'},
            {'input': '[10,20,30]', 'output': '60', 'explanation': 'Sum of all elements: 10+20+30 = 60'},
            {'input': '[]', 'output': '0', 'explanation': 'Empty array has sum 0'}
        ]
        problem.constraints = ['1 ≤ arr.length ≤ 1000', '-1000 ≤ arr[i] ≤ 1000']
        problem.test_cases = [
            {'input': '[1,2,3,4,5]', 'expected_output': '15'},
            {'input': '[10,20,30]', 'expected_output': '60'},
            {'input': '[]', 'expected_output': '0'},
            {'input': '[-1,-2,3]', 'expected_output': '0'}
        ]
    elif problem_id == 3:
        problem.examples = [
            {'input': '"hello"', 'output': 'olleh', 'explanation': 'Reverse of "hello" is "olleh"'},
            {'input': '"world"', 'output': 'dlrow', 'explanation': 'Reverse of "world" is "dlrow"'},
            {'input': '""', 'output': '""', 'explanation': 'Empty string reversed is empty string'}
        ]
        problem.constraints = ['1 ≤ s.length ≤ 100', 's consists of printable ASCII characters']
        problem.test_cases = [
            {'input': '"hello"', 'expected_output': 'olleh'},
            {'input': '"world"', 'expected_output': 'dlrow'},
            {'input': '""', 'expected_output': '""'},
            {'input': '"a"', 'expected_output': 'a'}
        ]
    elif problem_id == 4:
        problem.examples = [
            {'input': 'n=5', 'output': 'true', 'explanation': '5 is prime (divisible only by 1 and 5)'},
            {'input': 'n=4', 'output': 'false', 'explanation': '4 is not prime (divisible by 1, 2, 4)'},
            {'input': 'n=1', 'output': 'false', 'explanation': '1 is not considered prime'}
        ]
        problem.constraints = ['1 ≤ n ≤ 1000']
        problem.test_cases = [
            {'input': '5', 'expected_output': 'true'},
            {'input': '4', 'expected_output': 'false'},
            {'input': '1', 'expected_output': 'false'},
            {'input': '17', 'expected_output': 'true'}
        ]
    elif problem_id == 5:
        problem.examples = [
            {'input': '[1,2,3,1]', 'output': 'true', 'explanation': '1 appears twice in the array'},
            {'input': '[1,2,3,4]', 'output': 'false', 'explanation': 'No duplicates in the array'},
            {'input': '[1,1,1,3,3,4,3,2,4,2]', 'output': 'true', 'explanation': 'Multiple duplicates exist'}
        ]
        problem.constraints = ['1 ≤ nums.length ≤ 105', '-109 ≤ nums[i] ≤ 109']
        problem.test_cases = [
            {'input': '[1,2,3,1]', 'expected_output': 'true'},
            {'input': '[1,2,3,4]', 'expected_output': 'false'},
            {'input': '[1,1,1,3,3,4,3,2,4,2]', 'expected_output': 'true'},
            {'input': '[1]', 'expected_output': 'false'}
        ]
    elif problem_id == 6:
        problem.examples = [
            {'input': 'n=4', 'output': '2', 'explanation': 'There are 2 ways: (1,1,1,1) and (1,1,2)'},
            {'input': 'n=3', 'output': '3', 'explanation': 'There are 3 ways: (1,1,1), (1,2), (2,1)'},
            {'input': 'n=2', 'output': '2', 'explanation': 'There are 2 ways: (1,1), (2)'}
        ]
        problem.constraints = ['1 ≤ n ≤ 45']
        problem.test_cases = [
            {'input': '4', 'expected_output': '2'},
            {'input': '3', 'expected_output': '3'},
            {'input': '2', 'expected_output': '2'},
            {'input': '5', 'expected_output': '8'}
        ]
    
    return render(request, 'problems/problem_detail.html', {'problem': problem})

# Online Compiler Views
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

def my_submissions(request):
    """View to show user's own submissions"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    submissions = CodeSubmission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'compiler/my_submissions.html', {'submissions': submissions})

