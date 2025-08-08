#!/usr/bin/env python
"""
Test script to verify timer functionality
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from auth_app.models import Contest, ContestParticipation, User
from django.utils import timezone

def test_timer():
    """Test timer functionality"""
    print("Testing timer functionality...")
    
    # Get the active contest
    contest = Contest.objects.filter(is_active=True).first()
    if not contest:
        print("No active contest found!")
        return
    
    print(f"Active contest: {contest.title}")
    print(f"Start date: {contest.start_date}")
    print(f"End date: {contest.end_date}")
    print(f"Is running: {contest.is_running}")
    
    # Get a test user (first user in database)
    user = User.objects.first()
    if not user:
        print("No users found in database!")
        return
    
    print(f"Test user: {user.username}")
    
    # Check if user has participation
    participation = ContestParticipation.objects.filter(
        user=user,
        contest=contest,
        is_active=True
    ).first()
    
    if participation:
        print(f"User has active participation: {participation}")
        print(f"Participation start time: {participation.start_time}")
        print(f"Time remaining: {participation.time_remaining} seconds")
        print(f"Elapsed time: {participation.elapsed_time} seconds")
        
        # Convert to hours:minutes:seconds
        remaining_seconds = participation.time_remaining
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        seconds = remaining_seconds % 60
        
        print(f"Time remaining formatted: {hours:02d}:{minutes:02d}:{seconds:02d}")
    else:
        print("User has no active participation")
        
        # Check for inactive participation
        inactive_participation = ContestParticipation.objects.filter(
            user=user,
            contest=contest,
            is_active=False
        ).first()
        
        if inactive_participation:
            print(f"User has inactive participation: {inactive_participation}")
        else:
            print("User has no participation at all")

if __name__ == "__main__":
    test_timer()
