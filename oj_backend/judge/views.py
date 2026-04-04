from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.timezone import make_aware, get_current_timezone
from accounts.models import UserProfile
from .models import (
    Problem, Contest, Submission, TestCase,
    SubmissionResult, ContestParticipation,
)
from .forms import ProblemSubmissionForm, ProblemForm, ContestForm, TestCaseForm
from .judge_engine import OnlineJudge, TestCaseManager
import json
import logging

logger = logging.getLogger(__name__)


def update_leaderboard_ranks():
    """Update ranks for all users based on their scores"""
    profiles = UserProfile.objects.all().order_by('-score')
    for rank, profile in enumerate(profiles, 1):
        profile.rank = rank
        profile.save()


# ---------------------------------------------------------------------------
# Problem views
# ---------------------------------------------------------------------------

def problems_view(request):
    # Show all problems (including contest problems)
    problems = Problem.objects.all().order_by('id')

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
                    print(f"DEBUG: Submission marked as AC - updating scores for user {request.user.username}")
                    # Get or create user profile
                    user_profile, created = UserProfile.objects.get_or_create(
                        user=request.user,
                        defaults={'score': 0, 'rank': 0}
                    )

                    print(f"DEBUG: User profile - current score: {user_profile.score}, problems solved: {user_profile.problems_solved.count()}")

                    # Add problem to solved problems if not already solved
                    if problem not in user_profile.problems_solved.all():
                        print(f"DEBUG: Problem {problem.title} not previously solved - adding to solved problems")
                        user_profile.problems_solved.add(problem)

                        # Update score based on problem difficulty
                        difficulty_scores = {
                            'Easy': 10,
                            'Medium': 20,
                            'Hard': 30
                        }
                        score_increase = difficulty_scores.get(problem.difficulty, 10)
                        old_score = user_profile.score
                        user_profile.score += score_increase
                        user_profile.save()

                        print(f"DEBUG: Score updated: {old_score} -> {user_profile.score} (+{score_increase})")
                        print(f"DEBUG: Updating leaderboard ranks...")

                        # Update ranks for all users
                        update_leaderboard_ranks()
                        print(f"DEBUG: Leaderboard ranks updated")
                    else:
                        print(f"DEBUG: Problem {problem.title} already solved - no score increase")
                else:
                    print(f"DEBUG: Submission status is {result['status']} - no score update")

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
                            difficulty_scores = {
                                'Easy': 10,
                                'Medium': 20,
                                'Hard': 30
                            }
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


# ---------------------------------------------------------------------------
# Submission views
# ---------------------------------------------------------------------------

def submissions_view(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    else:
        submissions = []
    return render(request, 'submission/submissions.html', {'submissions': submissions})


def submission_detail_view(request, submission_id):
    """View detailed results of a submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    results = submission.results.all()

    context = {
        'submission': submission,
        'results': results
    }
    return render(request, 'submission/submission_detail.html', context)


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------

def leaderboard_view(request):
    logger.info("Leaderboard view called")

    # Get all user profiles ordered by score (highest first)
    user_profiles = UserProfile.objects.all().order_by('-score', 'user__username')

    # Update ranks for all users
    for rank, profile in enumerate(user_profiles, 1):
        if profile.rank != rank:
            profile.rank = rank
            profile.save()

    # Format data for the template
    leaderboard = []
    for profile in user_profiles:
        leaderboard.append({
            'username': profile.user.username,
            'score': profile.score,
            'problems_solved': profile.problems_solved.count(),
            'rank': profile.rank
        })

    context = {
        'leaderboard': leaderboard,
        'debug_info': {
            'user_count': user_profiles.count(),
            'leaderboard_length': len(leaderboard),
            'first_user': leaderboard[0] if leaderboard else None
        }
    }

    return render(request, 'leaderboard/leaderboard.html', context)


def test_leaderboard_data(request):
    """Test endpoint to verify leaderboard data generation"""
    user_profiles = UserProfile.objects.all().order_by('-score', 'user__username')

    leaderboard = []
    for profile in user_profiles:
        leaderboard.append({
            'username': profile.user.username,
            'score': profile.score,
            'problems_solved': profile.problems_solved.count(),
            'rank': profile.rank
        })

    return JsonResponse({
        'user_count': user_profiles.count(),
        'leaderboard_length': len(leaderboard),
        'leaderboard': leaderboard,
        'first_user': leaderboard[0] if leaderboard else None
    })


# ---------------------------------------------------------------------------
# Contest views
# ---------------------------------------------------------------------------

def contests_view(request):
    contests = Contest.objects.filter(is_active=True).order_by('-start_date')

    now = timezone.now()
    for contest in contests:
        if contest.start_date > now:
            contest.status = 'Upcoming'
            contest.time_remaining = None
        elif contest.end_date < now:
            contest.status = 'Ended'
            contest.time_remaining = None
        else:
            contest.status = 'Running'
            remaining = contest.end_date - now
            contest.time_remaining = int(remaining.total_seconds() / 3600)

        duration = contest.end_date - contest.start_date
        contest.duration_hours = int(duration.total_seconds() / 3600)

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


@login_required
def contest_detail(request, contest_id):
    """View contest details and problems"""
    contest = get_object_or_404(Contest, id=contest_id)
    problems = contest.problems.all()

    participation = ContestParticipation.objects.filter(
        user=request.user,
        contest=contest,
        is_active=True
    ).first()

    solved_problems = set()
    if participation:
        solved_problems = set(participation.problems_solved.all())

    for problem in problems:
        problem.is_solved = problem in solved_problems

    context = {
        'contest': contest,
        'problems': problems,
        'participation': participation
    }
    return render(request, 'contests/contest_detail.html', context)


@login_required
def start_contest(request, contest_id):
    """Start contest participation for a user"""
    contest = get_object_or_404(Contest, id=contest_id)

    if not contest.is_running:
        return JsonResponse({
            'success': False,
            'error': 'Contest is not currently running'
        })

    # Enforce registration cutoff
    try:
        tz = get_current_timezone()
        cutoff = make_aware(datetime(timezone.now().year, 8, 15, 23, 59, 59), tz)
    except Exception:
        cutoff = timezone.now()
    if timezone.now() > cutoff:
        return JsonResponse({
            'success': False,
            'error': 'Registration for this contest is closed.'
        })

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

    previously_ended = ContestParticipation.objects.filter(
        user=request.user,
        contest=contest,
        is_active=False,
        end_time__isnull=False
    ).exists()
    if previously_ended:
        return JsonResponse({
            'success': False,
            'error': 'You have already ended this contest and cannot re-enter.'
        })

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
    participation = get_object_or_404(
        ContestParticipation,
        user=request.user,
        contest_id=contest_id,
        is_active=True
    )

    participation.is_active = False
    participation.end_time = timezone.now()
    participation.save()

    return JsonResponse({
        'success': True,
        'final_score': participation.score
    })


# ---------------------------------------------------------------------------
# Admin views
# ---------------------------------------------------------------------------

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
    test_cases_qs = problem.test_cases.all()

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
        'test_cases': test_cases_qs,
        'form': form
    }
    return render(request, 'admin/manage_test_cases.html', context)


def create_sample_data(request):
    """Create sample problems and test cases for demonstration"""
    if not request.user.is_superuser:
        return redirect('home')

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
