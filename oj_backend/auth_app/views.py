from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db import IntegrityError
from .models import Problem, Contest, UserProfile, Submission, ConceptOfDay


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        except IntegrityError:
            # Username already exists
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
    # Get active contests
    contests = Contest.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('start_date')[:3]
    
    # Get today's concept
    today = timezone.now().date()
    concept_of_day = ConceptOfDay.objects.filter(date=today).first()
    
    # If no concept for today, get the latest one
    if not concept_of_day:
        concept_of_day = ConceptOfDay.objects.order_by('-date').first()
    
    # If still no concept, create a default one
    if not concept_of_day:
        concept_of_day = {
            'title': 'Dynamic Programming',
            'description': 'Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. It is applicable when the subproblems are not independent, that is, when subproblems share subsubproblems.'
        }
    
    # Get statistics
    total_problems = Problem.objects.count()
    total_contests = Contest.objects.filter(is_active=True).count()
    total_users = User.objects.count()
    total_submissions = Submission.objects.count()
    
    context = {
        'contests': contests,
        'concept_of_day': concept_of_day,
        'total_problems': total_problems,
        'total_contests': total_contests,
        'total_users': total_users,
        'total_submissions': total_submissions,
    }
    return render(request, 'home/home.html', context)

def problems_view(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problems.html', {'problems': problems})

def contests_view(request):
    contests = Contest.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'contests/contests.html', {'contests': contests})

def submissions_view(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    else:
        submissions = []
    return render(request, 'submission/submissions.html', {'submissions': submissions})

def leaderboard_view(request):
    # Get users ordered by score
    user_profiles = UserProfile.objects.all().order_by('-score')
    return render(request, 'leaderboard/leaderboard.html', {'user_profiles': user_profiles})

def problem_detail(request, problem_id):
    problems = [
        {
            'id': 1,
            'title': 'Two Sum',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'difficulty': 'Easy',
            'examples': [
                {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'nums[0] + nums[1] == 9'},
                {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]', 'explanation': 'nums[1] + nums[2] == 6'},
                {'input': 'nums = [3,3], target = 6', 'output': '[0,1]', 'explanation': 'nums[0] + nums[1] == 6'},
            ],
            'constraints': [
                '2 <= nums.length <= 10^4',
                '-10^9 <= nums[i] <= 10^9',
                '-10^9 <= target <= 10^9',
                'Only one valid answer exists.'
            ],
            'test_cases': [
                {'input': 'nums = [2,7,11,15]\ntarget = 9', 'expected_output': '[0,1]'},
                {'input': 'nums = [3,2,4]\ntarget = 6', 'expected_output': '[1,2]'},
            ]
        },
        {
            'id': 2,
            'title': 'Reverse Linked List',
            'description': 'Reverse a singly linked list.',
            'difficulty': 'Easy',
            'examples': [
                {'input': 'head = [1,2,3,4,5]', 'output': '[5,4,3,2,1]', 'explanation': 'Reverse the list.'},
                {'input': 'head = [1,2]', 'output': '[2,1]', 'explanation': 'Reverse the list.'},
                {'input': 'head = []', 'output': '[]', 'explanation': 'Empty list remains empty.'},
            ],
            'constraints': [
                'The number of nodes in the list is the range [0, 5000].',
                '-5000 <= Node.val <= 5000'
            ],
            'test_cases': [
                {'input': 'head = [1,2,3,4,5]', 'expected_output': '[5,4,3,2,1]'},
                {'input': 'head = [1,2]', 'expected_output': '[2,1]'},
            ]
        },
        {
            'id': 3,
            'title': 'Longest Substring Without Repeating Characters',
            'description': 'Given a string s, find the length of the longest substring without repeating characters.',
            'difficulty': 'Medium',
            'examples': [
                {'input': 's = "abcabcbb"', 'output': '3', 'explanation': 'The answer is "abc", with the length of 3.'},
                {'input': 's = "bbbbb"', 'output': '1', 'explanation': 'The answer is "b", with the length of 1.'},
                {'input': 's = "pwwkew"', 'output': '3', 'explanation': 'The answer is "wke", with the length of 3.'},
            ],
            'constraints': [
                '0 <= s.length <= 5 * 10^4',
                's consists of English letters, digits, symbols and spaces.'
            ],
            'test_cases': [
                {'input': 's = "abcabcbb"', 'expected_output': '3'},
                {'input': 's = "bbbbb"', 'expected_output': '1'},
            ]
        },
        {
            'id': 4,
            'title': 'Add Two Numbers',
            'description': 'You are given two non-empty linked lists representing two non-negative integers. Add the two numbers and return the sum as a linked list.',
            'difficulty': 'Medium',
            'examples': [
                {'input': 'l1 = [2,4,3], l2 = [5,6,4]', 'output': '[7,0,8]', 'explanation': '342 + 465 = 807.'},
                {'input': 'l1 = [0], l2 = [0]', 'output': '[0]', 'explanation': '0 + 0 = 0.'},
                {'input': 'l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]', 'output': '[8,9,9,9,0,0,0,1]', 'explanation': '9999999 + 9999 = 10009998.'},
            ],
            'constraints': [
                'The number of nodes in each linked list is in the range [1, 100].',
                '0 <= Node.val <= 9',
                'It is guaranteed that the list represents a number that does not have leading zeros.'
            ],
            'test_cases': [
                {'input': 'l1 = [2,4,3], l2 = [5,6,4]', 'expected_output': '[7,0,8]'},
                {'input': 'l1 = [0], l2 = [0]', 'expected_output': '[0]'},
            ]
        },
        {
            'id': 5,
            'title': 'Median of Two Sorted Arrays',
            'description': 'Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.',
            'difficulty': 'Hard',
            'examples': [
                {'input': 'nums1 = [1,3], nums2 = [2]', 'output': '2.0', 'explanation': 'The median is 2.0.'},
                {'input': 'nums1 = [1,2], nums2 = [3,4]', 'output': '2.5', 'explanation': 'The median is (2 + 3)/2 = 2.5.'},
                {'input': 'nums1 = [0,0], nums2 = [0,0]', 'output': '0.0', 'explanation': 'The median is 0.0.'},
            ],
            'constraints': [
                'nums1.length == m',
                'nums2.length == n',
                '0 <= m <= 1000',
                '0 <= n <= 1000',
                '1 <= m + n <= 2000',
                '-10^6 <= nums1[i], nums2[i] <= 10^6'
            ],
            'test_cases': [
                {'input': 'nums1 = [1,3], nums2 = [2]', 'expected_output': '2.0'},
                {'input': 'nums1 = [1,2], nums2 = [3,4]', 'expected_output': '2.5'},
            ]
        },
        {
            'id': 6,
            'title': 'Regular Expression Matching',
            'description': 'Given an input string s and a pattern p, implement regular expression matching with support for . and *.',
            'difficulty': 'Hard',
            'examples': [
                {'input': 's = "aa", p = "a"', 'output': 'false', 'explanation': '"a" does not match the entire string "aa".'},
                {'input': 's = "aa", p = "a*"', 'output': 'true', 'explanation': '"*" means zero or more of the preceding element, so "aa" is matched as "a*".'},
                {'input': 's = "ab", p = ".*"', 'output': 'true', 'explanation': '".*" means zero or more of any character.'},
            ],
            'constraints': [
                '1 <= s.length <= 20',
                '1 <= p.length <= 30',
                's contains only lowercase English letters.',
                'p contains only lowercase English letters, ".", and "*".'
            ],
            'test_cases': [
                {'input': 's = "aa", p = "a"', 'expected_output': 'false'},
                {'input': 's = "aa", p = "a*"', 'expected_output': 'true'},
            ]
        },
    ]
    problem = next((p for p in problems if p['id'] == problem_id), None)
    if not problem:
        from django.http import Http404
        raise Http404("No Problem matches the given query.")
    return render(request, 'problems/problem_detail.html', {'problem': problem})

