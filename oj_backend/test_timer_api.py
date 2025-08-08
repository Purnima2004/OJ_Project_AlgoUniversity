#!/usr/bin/env python
"""
Test timer API directly
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from auth_app.models import Contest, ContestParticipation, User
from django.utils import timezone
from django.test import RequestFactory
from auth_app.views import get_contest_timer
import json

def test_timer_api():
    """Test timer API directly"""
    print("Testing timer API...")
    
    # Get the active contest
    contest = Contest.objects.filter(is_active=True).first()
    if not contest:
        print("No active contest found!")
        return
    
    # Get the user with participation
    user = User.objects.filter(username='purnimasahoo2022@vitbhopal.ac.in').first()
    if not user:
        print("User not found!")
        return
    
    print(f"Testing timer for user: {user.username}")
    print(f"Contest: {contest.title}")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get(f'/auth/contest/{contest.id}/timer/')
    request.user = user
    
    # Call the timer view
    try:
        response = get_contest_timer(request, contest.id)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        # Parse JSON response
        data = json.loads(response.content.decode())
        print(f"Success: {data.get('success')}")
        if data.get('success'):
            print(f"Time remaining: {data.get('time_remaining')} seconds")
            print(f"Elapsed time: {data.get('elapsed_time')} seconds")
            
            # Convert to HH:MM:SS
            remaining = data.get('time_remaining', 0)
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            print(f"Formatted time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            print(f"Error: {data.get('error')}")
            
    except Exception as e:
        print(f"Error calling timer API: {e}")

if __name__ == "__main__":
    test_timer_api()
