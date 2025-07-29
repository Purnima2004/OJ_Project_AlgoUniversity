from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Problem

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'auth_app/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'auth_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    # Hardcoded problems for frontend display
    problems = [
        {'id': 1, 'title': 'Two Sum', 'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'difficulty': 'Easy'},
        {'id': 2, 'title': 'Reverse Linked List', 'description': 'Reverse a singly linked list.', 'difficulty': 'Easy'},
        {'id': 3, 'title': 'Longest Substring Without Repeating Characters', 'description': 'Given a string s, find the length of the longest substring without repeating characters.', 'difficulty': 'Medium'},
        {'id': 4, 'title': 'Add Two Numbers', 'description': 'You are given two non-empty linked lists representing two non-negative integers. Add the two numbers and return the sum as a linked list.', 'difficulty': 'Medium'},
        {'id': 5, 'title': 'Median of Two Sorted Arrays', 'description': 'Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays.', 'difficulty': 'Hard'},
        {'id': 6, 'title': 'Regular Expression Matching', 'description': 'Given an input string s and a pattern p, implement regular expression matching with support for . and *.', 'difficulty': 'Hard'},
    ]
    return render(request, 'auth_app/home.html', {'problems': problems})
# ... existing code ...
def problem_detail(request, problem_id):
    # Use the same hardcoded problems as in home()
    problems = [
        {'id': 1, 'title': 'Two Sum', 'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'difficulty': 'Easy'},
        {'id': 2, 'title': 'Reverse Linked List', 'description': 'Reverse a singly linked list.', 'difficulty': 'Easy'},
        {'id': 3, 'title': 'Longest Substring Without Repeating Characters', 'description': 'Given a string s, find the length of the longest substring without repeating characters.', 'difficulty': 'Medium'},
        {'id': 4, 'title': 'Add Two Numbers', 'description': 'You are given two non-empty linked lists representing two non-negative integers. Add the two numbers and return the sum as a linked list.', 'difficulty': 'Medium'},
        {'id': 5, 'title': 'Median of Two Sorted Arrays', 'description': 'Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays.', 'difficulty': 'Hard'},
        {'id': 6, 'title': 'Regular Expression Matching', 'description': 'Given an input string s and a pattern p, implement regular expression matching with support for . and *.', 'difficulty': 'Hard'},
    ]
    problem = next((p for p in problems if p['id'] == problem_id), None)
    if not problem:
        from django.http import Http404
        raise Http404("No Problem matches the given query.")
    return render(request, 'auth_app/problem_detail.html', {'problem': problem})

