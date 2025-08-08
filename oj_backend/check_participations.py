#!/usr/bin/env python
"""
Check participations in database
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

def check_participations():
    """Check all participations in database"""
    print("Checking participations in database...")
    
    # Get all participations
    participations = ContestParticipation.objects.all()
    
    if participations.exists():
        print(f"Found {participations.count()} participations:")
        for participation in participations:
            print(f"  - User: {participation.user.username}")
            print(f"    Contest: {participation.contest.title}")
            print(f"    Active: {participation.is_active}")
            print(f"    Start Time: {participation.start_time}")
            print(f"    End Time: {participation.end_time}")
            print(f"    Score: {participation.score}")
            print("    ---")
    else:
        print("No participations found in database.")
    
    # Get active contest
    contest = Contest.objects.filter(is_active=True).first()
    if contest:
        print(f"\nActive contest: {contest.title}")
        print(f"Start date: {contest.start_date}")
        print(f"End date: {contest.end_date}")
        print(f"Is running: {contest.is_running}")
        
        # Check participations for this contest
        contest_participations = ContestParticipation.objects.filter(contest=contest)
        print(f"\nParticipations for this contest: {contest_participations.count()}")
        for participation in contest_participations:
            print(f"  - User: {participation.user.username}, Active: {participation.is_active}")

if __name__ == "__main__":
    check_participations()
