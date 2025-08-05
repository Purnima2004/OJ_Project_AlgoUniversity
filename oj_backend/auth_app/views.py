from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Problem, Contest, UserProfile, Submission, ConceptOfDay, CodeSubmission, TestCase, SubmissionResult
from .forms import CodeSubmissionForm, ProblemSubmissionForm, ContestForm, ProblemForm, TestCaseForm
from .compiler import CodeCompiler
from .oj_system import OnlineJudge, TestCaseManager
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
    test_cases = list(problem.test_cases.filter(is_sample=True))
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ProblemSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            submission.save()
            
            # Judge the submission
            oj = OnlineJudge()
            result = oj.judge_submission(submission)
            
            return JsonResponse({
                'success': True,
                'status': result['status'],
                'test_cases_passed': result['test_cases_passed'],
                'total_test_cases': result['total_test_cases'],
                'execution_time': result.get('execution_time', 0),
                'error_message': result.get('error_message', '')
            })
    else:
        form = ProblemSubmissionForm()
    
    context = {
        'problem': problem,
        'form': form,
        'test_cases': test_cases
    }
    return render(request, 'problems/problem_detail.html', context)

@csrf_exempt  # Allow AJAX from unauthenticated users for run mode
@login_required
def submit_solution(request, problem_id):
    """Handle solution submission via AJAX. Supports 'run' and 'submit' modes."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            problem = get_object_or_404(Problem, id=problem_id)
            mode = data.get('mode', 'submit')
            code = data.get('code', '')
            language = data.get('language', 'python')
            if mode == 'run':
                # Judge only sample test cases, do not save submission
                class TempSubmission:
                    def __init__(self, user, problem, code, language):
                        self.user = user
                        self.problem = problem
                        self.code = code
                        self.language = language
                        self.status = None
                        self.test_cases_passed = 0
                        self.total_test_cases = 0
                        self.error_message = ''
                        self.execution_time = 0
                        self.memory_used = 0
                temp_submission = TempSubmission(request.user, problem, code, language)
                oj = OnlineJudge()
                # Only sample test cases
                sample_cases = problem.test_cases.filter(is_sample=True)
                result = oj.judge_submission(temp_submission, test_cases=sample_cases)
                return JsonResponse({
                    'success': True,
                    'status': result['status'],
                    'test_cases_passed': result['test_cases_passed'],
                    'total_test_cases': result['total_test_cases'],
                    'execution_time': result.get('execution_time', 0),
                    'error_message': result.get('error_message', ''),
                    'test_cases': result.get('test_cases', [])
                })
            else:
                # Normal submit: save submission and judge all test cases
                submission = Submission.objects.create(
                    user=request.user,
                    problem=problem,
                    code=code,
                    language=language
                )
                oj = OnlineJudge()
                result = oj.judge_submission(submission)
                return JsonResponse({
                    'success': True,
                    'submission_id': submission.id,
                    'status': result['status'],
                    'test_cases_passed': result['test_cases_passed'],
                    'total_test_cases': result['total_test_cases'],
                    'execution_time': result.get('execution_time', 0),
                    'error_message': result.get('error_message', ''),
                    'test_cases': result.get('test_cases', [])
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def submission_detail_view(request, submission_id):
    """View detailed results of a submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    results = submission.results.all()
    
    context = {
        'submission': submission,
        'results': results
    }
    return render(request, 'submission/submission_detail.html', context)

@login_required
def contest_detail(request, contest_id):
    """View contest details and problems"""
    contest = get_object_or_404(Contest, id=contest_id)
    problems = contest.problems.all()
    
    context = {
        'contest': contest,
        'problems': problems
    }
    return render(request, 'contests/contest_detail.html', context)

# Admin views for managing problems and contests
@login_required
def create_problem(request):
    """Create a new problem"""
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            return redirect('problem_detail', problem_id=problem.id)
    else:
        form = ProblemForm()
    
    return render(request, 'admin/create_problem.html', {'form': form})

@login_required
def create_contest(request):
    """Create a new contest"""
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save()
            return redirect('contest_detail', contest_id=contest.id)
    else:
        form = ContestForm()
    
    return render(request, 'admin/create_contest.html', {'form': form})

@login_required
def manage_test_cases(request, problem_id):
    """Manage test cases for a problem"""
    if not request.user.is_superuser:
        return redirect('home')
    
    problem = get_object_or_404(Problem, id=problem_id)
    test_cases = problem.test_cases.all()
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.problem = problem
            test_case.save()
            return redirect('manage_test_cases', problem_id=problem_id)
    else:
        form = TestCaseForm()
    
    context = {
        'problem': problem,
        'test_cases': test_cases,
        'form': form
    }
    return render(request, 'admin/manage_test_cases.html', context)

def create_sample_data(request):
    """Create sample problems and test cases for demonstration"""
    if not request.user.is_superuser:
        return redirect('home')
    
    # Create sample problems
    problems_data = [
        {
            'title': 'Two Sum',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'difficulty': 'Easy',
            'examples': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].',
            'constraints': '2 <= nums.length <= 104\n-109 <= nums[i] <= 109\n-109 <= target <= 109',
            'time_limit': 1000,
            'memory_limit': 256
        },
        {
            'title': 'Add Two Numbers',
            'description': 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.',
            'difficulty': 'Medium',
            'examples': 'Input: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [7,0,8]\nExplanation: 342 + 465 = 807.',
            'constraints': 'The number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros.',
            'time_limit': 1000,
            'memory_limit': 256
        },
        {
            'title': 'Longest Substring Without Repeating Characters',
            'description': 'Given a string s, find the length of the longest substring without repeating characters.',
            'difficulty': 'Medium',
            'examples': 'Input: s = "abcabcbb"\nOutput: 3\nExplanation: The answer is "abc", with the length of 3.',
            'constraints': '0 <= s.length <= 5 * 104\ns consists of English letters, digits, symbols and spaces.',
            'time_limit': 1000,
            'memory_limit': 256
        }
    ]
    
    for data in problems_data:
        problem, created = Problem.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
    
    # Create sample test cases
    TestCaseManager.create_sample_test_cases()
    
    return redirect('problems')

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

