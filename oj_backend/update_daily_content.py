#!/usr/bin/env python
"""
Daily content update script for OJ Project
This script updates contests and concept of the day
"""

import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone

def update_daily_content():
    """Update contests and concept of the day"""
    print(f"Starting daily content update at {timezone.now()}")
    
    try:
        # Update concept of the day
        print("Updating concept of the day...")
        call_command('update_concept_of_day')
        
        # Update contests (only if needed)
        print("Checking contests...")
        call_command('update_contests')
        
        print("Daily content update completed successfully!")
        
    except Exception as e:
        print(f"Error during daily content update: {e}")
        return False
    
    return True

if __name__ == "__main__":
    update_daily_content() 