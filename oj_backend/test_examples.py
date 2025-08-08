#!/usr/bin/env python
"""
Test script to verify contest problem examples are working correctly
"""

import os
import sys
import django
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from auth_app.models import Problem

def test_examples():
    """Test that examples are stored and retrieved correctly"""
    print("Testing contest problem examples...")
    
    contest_problems = Problem.objects.filter(title__icontains='Contest')
    
    for problem in contest_problems:
        print(f"\nProblem: {problem.title}")
        print(f"Difficulty: {problem.difficulty}")
        
        # Test examples
        try:
            examples = json.loads(problem.examples) if problem.examples else []
            print(f"Examples count: {len(examples)}")
            for i, example in enumerate(examples, 1):
                print(f"  Example {i}: {example[:100]}...")
        except json.JSONDecodeError as e:
            print(f"Error parsing examples: {e}")
            print(f"Raw examples: {problem.examples}")
        
        # Test constraints
        try:
            constraints = json.loads(problem.constraints) if problem.constraints else []
            print(f"Constraints count: {len(constraints)}")
            for i, constraint in enumerate(constraints, 1):
                print(f"  Constraint {i}: {constraint}")
        except json.JSONDecodeError as e:
            print(f"Error parsing constraints: {e}")
            print(f"Raw constraints: {problem.constraints}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_examples() 