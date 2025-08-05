#!/usr/bin/env python
"""
Test script for the OJ system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from auth_app.oj_system import OnlineJudge, TestCaseManager
from auth_app.models import Problem, TestCase

def test_two_sum():
    """Test the Two Sum problem"""
    print("=== Testing Two Sum Problem ===")
    
    # Get the Two Sum problem
    problem = Problem.objects.filter(title="Two Sum").first()
    if not problem:
        print("Two Sum problem not found!")
        return
    
    print(f"Problem: {problem.title}")
    
    # Get test cases
    test_cases = problem.test_cases.all()
    print(f"Found {test_cases.count()} test cases")
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Input: '{test_case.input_data}'")
        print(f"Expected: '{test_case.expected_output}'")
        print(f"Is Sample: {test_case.is_sample}")
        
        # Test with correct solution
        test_code = """
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return []

# Read input
first_line = input().split()
n = int(first_line[0])
nums = [int(first_line[i]) for i in range(1, n + 1)]
target = int(input())

# Solve and print result
result = two_sum(nums, target)
print(result[0], result[1])
"""
        
        # Create a temporary submission object
        class TempSubmission:
            def __init__(self, problem, code):
                self.problem = problem
                self.code = code
                self.language = 'python'
        
        temp_submission = TempSubmission(problem, test_code)
        
        # Test with OJ
        oj = OnlineJudge()
        result = oj.judge_submission(temp_submission, test_cases=[test_case])
        
        print(f"OJ Result: {result}")
        print(f"Status: {result.get('status')}")
        print(f"Test cases passed: {result.get('test_cases_passed')}/{result.get('total_test_cases')}")
        
        if result.get('test_cases'):
            for j, tc_result in enumerate(result['test_cases']):
                print(f"  Test case {j+1}: {tc_result['status']}")
                print(f"    Actual output: '{tc_result['actual_output']}'")
                print(f"    Error: '{tc_result['error_message']}'")

if __name__ == "__main__":
    test_two_sum() 