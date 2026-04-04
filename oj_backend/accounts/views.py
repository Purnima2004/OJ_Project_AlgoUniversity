from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import UserProfile
from .decorators import redirect_if_authenticated


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
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate required fields
        if not username or not password1 or not password2:
            return render(request, 'accounts/register.html', {
                'error': 'Please fill in all fields.'
            })

        # Check if passwords match
        if password1 != password2:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match.'
            })

        try:
            user = User.objects.create_user(username=username, password=password1)
            # Create user profile
            ensure_user_profile(user)
            login(request, user)
            return redirect('home')
        except IntegrityError:
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists. Please choose a different username.'
            })
    return render(request, 'accounts/register.html')


@redirect_if_authenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'accounts/login.html', {
                'error': 'Please provide both username and password.'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password. Please try again.'
            })
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
