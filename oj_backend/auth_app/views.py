from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Problem, Contest, UserProfile, Submission, ConceptOfDay, CodeSubmission, TestCase, SubmissionResult, ContestParticipation
from .forms import CodeSubmissionForm, ProblemSubmissionForm, ContestForm, ProblemForm, TestCaseForm
from .compiler import CodeCompiler
from .oj_system import OnlineJudge, TestCaseManager
from .decorators import redirect_if_authenticated
import json
import os
import subprocess
import tempfile
import uuid
import time
import psutil
from pathlib import Path
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-api-key-here')  # Set your API key in environment variables

# Debug: Print API key status (remove in production)
if GOOGLE_API_KEY == 'your-api-key-here':
    print("⚠️  WARNING: Using default API key. Please set GOOGLE_API_KEY environment variable.")
else:
    print(f"✅ API Key loaded: {GOOGLE_API_KEY[:10]}...")

genai.configure(api_key=GOOGLE_API_KEY)



def update_leaderboard_ranks():
    """Update ranks for all users based on their scores"""
    profiles = UserProfile.objects.all().order_by('-score')
    for rank, profile in enumerate(profiles, 1):
        profile.rank = rank
        profile.save()

def ensure_user_profile(user):
    """Ensure a user has a UserProfile"""
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'score': 0, 'rank': 0}
    )
    return user_profile

@redirect_if_authenticated
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            # Create user profile
            ensure_user_profile(user)
            login(request, user)
            return redirect('home')
        except IntegrityError:
            return render(request, 'register/register.html', {
                'error': 'Username already exists. Please choose a different username.'
            })
    return render(request, 'register/register.html')

@redirect_if_authenticated
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
    return redirect('home')

def home(request):
    # If user is not authenticated, show landing page
    if not request.user.is_authenticated:
        return render(request, 'landing/landing.html')
    
    # If user is authenticated, show dashboard
    now = timezone.now()
    active_contests = Contest.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )[:3]
    active_contests_count = Contest.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).count()
    concept_of_day = ConceptOfDay.objects.first()
    
    if not concept_of_day:
        concept_of_day = {
            'title': 'Dynamic Programming',
            'description': 'Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. It is applicable when the subproblems are not independent, that is, when subproblems share subsubproblems.',
            'example_code': 'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)'
        }
    
    context = {
        'contests': active_contests,
        'active_contests_count': active_contests_count,
        'concept_of_day': concept_of_day,
        'total_problems': Problem.objects.count(),
        'total_users': User.objects.count(),
        'total_submissions': Submission.objects.count(),
    }
    return render(request, 'home/home.html', context)

def problems_view(request):
    # Exclude contest problems (those with "Contest" in title)
    problems = Problem.objects.exclude(title__icontains='Contest')
    
    # Get user's solved problems if authenticated
    solved_problems = set()
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            solved_problems = set(user_profile.problems_solved.all())
        except UserProfile.DoesNotExist:
            pass
    
    # Add solved status to each problem
    for problem in problems:
        problem.is_solved = problem in solved_problems
    
    return render(request, 'problems/problems.html', {'problems': problems})

def contests_view(request):
    contests = Contest.objects.filter(is_active=True).order_by('-start_date')
    
    # Get user's active contest participation
    active_participation = None
    if request.user.is_authenticated:
        active_participation = ContestParticipation.objects.filter(
            user=request.user,
            is_active=True
        ).first()
    
    context = {
        'contests': contests,
        'active_participation': active_participation
    }
    return render(request, 'contests/contests.html', context)

def submissions_view(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    else:
        submissions = []
    return render(request, 'submission/submissions.html', {'submissions': submissions})

def leaderboard_view(request):
    # Get all user profiles ordered by score (highest first)
    user_profiles = UserProfile.objects.all().order_by('-score', 'user__username')
    
    
    for rank, profile in enumerate(user_profiles, 1):
        if profile.rank != rank:
            profile.rank = rank
            profile.save()
    
    return render(request, 'leaderboard/leaderboard.html', {'user_profiles': user_profiles})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    test_cases = list(problem.test_cases.filter(is_sample=True))
    
    # Check if this is a contest problem
    contest_id = request.GET.get('contest')
    contest = None
    if contest_id:
        try:
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            contest = None
    
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
        'test_cases': test_cases,
        'contest': contest
    }
    
    # Use contest template if accessed from contest
    if contest:
        return render(request, 'contests/contest_problem_detail.html', context)
    else:
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
                
                # Update user profile and scores if submission is successful
                if result['status'] == 'AC':
                    # Get or create user profile
                    user_profile, created = UserProfile.objects.get_or_create(
                        user=request.user,
                        defaults={'score': 0, 'rank': 0}
                    )
                    
                    # Add problem to solved problems if not already solved
                    if problem not in user_profile.problems_solved.all():
                        user_profile.problems_solved.add(problem)
                        
                        # Update score based on problem difficulty
                        difficulty_scores = {
                            'Easy': 10,
                            'Medium': 20,
                            'Hard': 30
                        }
                        score_increase = difficulty_scores.get(problem.difficulty, 10)
                        user_profile.score += score_increase
                        user_profile.save()
                        
                        # Update ranks for all users
                        update_leaderboard_ranks()
                    
                    # Update contest participation if this is a contest submission
                    contest_id = data.get('contest_id')
                    if contest_id:
                        try:
                            participation = ContestParticipation.objects.get(
                                user=request.user,
                                contest_id=contest_id,
                                is_active=True
                            )
                            
                            # Add problem to contest solved problems if not already solved
                            if problem not in participation.problems_solved.all():
                                participation.problems_solved.add(problem)
                                
                                # Update contest score
                                contest_score_increase = difficulty_scores.get(problem.difficulty, 10)
                                participation.score += contest_score_increase
                                participation.save()
                                
                        except ContestParticipation.DoesNotExist:
                            pass  # Not participating in contest
                
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
    
    # Get user's ACTIVE participation only
    participation = ContestParticipation.objects.filter(
        user=request.user,
        contest=contest,
        is_active=True
    ).first()
    
    # Get user's solved problems in this contest
    solved_problems = set()
    if participation:
        solved_problems = set(participation.problems_solved.all())
    
    # Add solved status to each problem
    for problem in problems:
        problem.is_solved = problem in solved_problems
    
    context = {
        'contest': contest,
        'problems': problems,
        'participation': participation
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
        
        # Check if the compilation/execution was successful
        is_success = result.get('status') in ['success']
        
        return JsonResponse({
            'success': is_success,
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

@login_required
def start_contest(request, contest_id):
    """Start contest participation for a user"""
    contest = get_object_or_404(Contest, id=contest_id)
    
    # Check if contest is running
    if not contest.is_running:
        return JsonResponse({
            'success': False,
            'error': 'Contest is not currently running'
        })
    
    # Check if user already has an active participation
    existing_participation = ContestParticipation.objects.filter(
        user=request.user,
        contest=contest,
        is_active=True
    ).first()
    
    if existing_participation:
        return JsonResponse({
            'success': False,
            'error': 'You are already participating in this contest'
        })
    
    # Check if user has an inactive participation and reactivate it
    inactive_participation = ContestParticipation.objects.filter(
        user=request.user,
        contest=contest,
        is_active=False
    ).first()
    
    if inactive_participation:
        # Reactivate the participation
        inactive_participation.is_active = True
        inactive_participation.start_time = timezone.now()
        inactive_participation.end_time = None
        inactive_participation.save()
        participation = inactive_participation
    else:
        # Create new participation
        participation = ContestParticipation.objects.create(
            user=request.user,
            contest=contest,
            is_active=True
        )
    
    return JsonResponse({
        'success': True,
        'participation_id': participation.id,
        'start_time': participation.start_time.isoformat(),
        'contest_end': contest.end_date.isoformat()
    })

@login_required
def get_contest_timer(request, contest_id):
    """Get remaining time for contest participation"""
    try:
        participation = ContestParticipation.objects.get(
            user=request.user, 
            contest_id=contest_id,
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'time_remaining': participation.time_remaining,
            'elapsed_time': participation.elapsed_time
        })
    except ContestParticipation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User has not started this contest'
        })

@login_required
def end_contest(request, contest_id):
    """End contest participation"""
    participation = get_object_or_404(ContestParticipation, 
                                    user=request.user, 
                                    contest_id=contest_id,
                                    is_active=True)
    
    participation.is_active = False
    participation.end_time = timezone.now()
    participation.save()
    
    return JsonResponse({
        'success': True,
        'final_score': participation.score
    })

@csrf_exempt
@login_required
def ai_review(request):
    """AI Review endpoint for code analysis using Gemini"""
    if request.method == 'POST':
        try:
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
                # Try the newer model name first
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(prompt)
            except Exception as e:
                # Fallback to older model name
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                except Exception as e2:
                    # If both fail, try the latest model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
            
            # Extract the response text
            if hasattr(response, 'text') and response.text:
                review_text = response.text
            else:
                review_text = "Unable to generate review at this time."
                
            print(f"✅ AI Review generated successfully with model")
            
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

