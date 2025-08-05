import os
import time
import logging
from typing import Dict, List, Any, Tuple
from .compiler import CodeCompiler
from .models import Problem, TestCase, Submission, SubmissionResult

logger = logging.getLogger(__name__)

class OnlineJudge:
    """Online Judge system for evaluating code submissions"""
    
    def __init__(self):
        self.compiler = CodeCompiler()
    
    def judge_submission(self, submission, test_cases=None):
        """Judge a submission against provided test cases (or all if not specified)"""
        try:
            problem = submission.problem
            if test_cases is None:
                test_cases = problem.test_cases.all()
            if not test_cases.exists():
                return {
                    'status': 'CE',
                    'error_message': 'No test cases available for this problem',
                    'test_cases_passed': 0,
                    'total_test_cases': 0
                }
            total_test_cases = len(test_cases)
            passed_test_cases = 0
            results = []
            for test_case in test_cases:
                result = self._run_test_case(submission, test_case)
                results.append(result)
                if result['status'] == 'AC':
                    passed_test_cases += 1
                elif result['status'] in ['TLE', 'RE', 'CE', 'MLE']:
                    break
            overall_status = self._determine_overall_status(results)
            # Only update DB fields if this is a real Submission instance
            if hasattr(submission, 'save'):
                submission.status = overall_status
                submission.test_cases_passed = passed_test_cases
                submission.total_test_cases = total_test_cases
                submission.error_message = self._get_error_message(results)
                execution_times = [r['execution_time'] for r in results if r['execution_time']]
                if execution_times:
                    submission.execution_time = sum(execution_times) / len(execution_times)
                memory_usage = [r['memory_used'] for r in results if r['memory_used']]
                if memory_usage:
                    submission.memory_used = sum(memory_usage) / len(memory_usage)
                submission.save()
                self._save_test_case_results(submission, results)
            # Prepare test case details for frontend
            test_case_details = []
            for i, result in enumerate(results):
                test_case = test_cases[i] if i < len(test_cases) else None
                test_case_details.append({
                    'input_data': test_case.input_data if test_case else '',
                    'expected_output': test_case.expected_output if test_case else '',
                    'actual_output': result['actual_output'],
                    'status': result['status'],
                    'execution_time': result['execution_time'],
                    'memory_used': result['memory_used'],
                    'error_message': result['error_message']
                })
            return {
                'status': overall_status,
                'test_cases_passed': passed_test_cases,
                'total_test_cases': total_test_cases,
                'execution_time': getattr(submission, 'execution_time', 0),
                'memory_used': getattr(submission, 'memory_used', 0),
                'error_message': getattr(submission, 'error_message', ''),
                'test_cases': test_case_details
            }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error judging submission: {str(e)}")
            if hasattr(submission, 'save'):
                submission.status = 'RE'
                submission.error_message = f"Judging error: {str(e)}"
                submission.save()
            return {
                'status': 'RE',
                'error_message': f"Judging error: {str(e)}",
                'test_cases_passed': 0,
                'total_test_cases': 0
            }
    
    def _run_test_case(self, submission: Submission, test_case: TestCase) -> Dict[str, Any]:
        """Run a single test case"""
        try:
            # Debug: Print test case details
            print(f"DEBUG: Running test case {test_case.id}")
            print(f"DEBUG: Input data: '{test_case.input_data}'")
            print(f"DEBUG: Expected output: '{test_case.expected_output}'")
            
            # Compile and run the code
            result = self.compiler.compile_and_run(
                code=submission.code,
                language=submission.language,
                input_data=test_case.input_data
            )
            
            print(f"DEBUG: Compiler result: {result}")
            
            # Check if compilation failed
            if result['status'] == 'error' or result['status'] == 'compilation_error':
                return {
                    'status': 'CE',
                    'execution_time': 0,
                    'memory_used': 0,
                    'actual_output': '',
                    'error_message': result['error']
                }
            
            # Check time limit
            if result['execution_time'] and result['execution_time'] * 1000 > submission.problem.time_limit:
                return {
                    'status': 'TLE',
                    'execution_time': result['execution_time'],
                    'memory_used': result.get('memory_used', 0),
                    'actual_output': result['output'],
                    'error_message': 'Time limit exceeded'
                }
            
            # Check memory limit (if available)
            if result.get('memory_used') and result['memory_used'] > submission.problem.memory_limit * 1024:
                return {
                    'status': 'MLE',
                    'execution_time': result['execution_time'],
                    'memory_used': result['memory_used'],
                    'actual_output': result['output'],
                    'error_message': 'Memory limit exceeded'
                }
            
            # Check if output matches expected
            if self._compare_output(result['output'], test_case.expected_output):
                return {
                    'status': 'AC',
                    'execution_time': result['execution_time'],
                    'memory_used': result.get('memory_used', 0),
                    'actual_output': result['output'],
                    'error_message': ''
                }
            else:
                return {
                    'status': 'WA',
                    'execution_time': result['execution_time'],
                    'memory_used': result.get('memory_used', 0),
                    'actual_output': result['output'],
                    'error_message': 'Wrong answer'
                }
                
        except Exception as e:
            logger.error(f"Error running test case {test_case.id}: {str(e)}")
            return {
                'status': 'RE',
                'execution_time': 0,
                'memory_used': 0,
                'actual_output': '',
                'error_message': f"Runtime error: {str(e)}"
            }
    
    def _compare_output(self, actual: str, expected: str) -> bool:
        """Compare actual output with expected output"""
        # Normalize whitespace and line endings
        actual_normalized = self._normalize_output(actual)
        expected_normalized = self._normalize_output(expected)
        
        # Debug output comparison
        print(f"DEBUG: Comparing outputs")
        print(f"Actual (raw): '{actual}'")
        print(f"Expected (raw): '{expected}'")
        print(f"Actual (normalized): '{actual_normalized}'")
        print(f"Expected (normalized): '{expected_normalized}'")
        print(f"Match: {actual_normalized == expected_normalized}")
        
        return actual_normalized == expected_normalized
    
    def _normalize_output(self, output: str) -> str:
        """Normalize output for comparison"""
        if not output:
            return ""
        
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in output.split('\n')]
        
        # Remove empty lines from end
        while lines and not lines[-1]:
            lines.pop()
        
        return '\n'.join(lines)
    
    def _determine_overall_status(self, results: List[Dict[str, Any]]) -> str:
        """Determine overall submission status based on test case results"""
        if not results:
            return 'WA'
        
        # Check for serious errors first
        for result in results:
            if result['status'] in ['TLE', 'RE', 'CE', 'MLE']:
                return result['status']
        
        # Check if all test cases passed
        all_passed = all(result['status'] == 'AC' for result in results)
        
        return 'AC' if all_passed else 'WA'
    
    def _get_error_message(self, results: List[Dict[str, Any]]) -> str:
        """Get error message from results"""
        for result in results:
            if result['error_message']:
                return result['error_message']
        return ""
    
    def _save_test_case_results(self, submission: Submission, results: List[Dict[str, Any]]):
        """Save individual test case results"""
        test_cases = submission.problem.test_cases.all()
        
        # Clear existing results
        SubmissionResult.objects.filter(submission=submission).delete()
        
        # Save new results
        for i, result in enumerate(results):
            if i < len(test_cases):
                SubmissionResult.objects.create(
                    submission=submission,
                    test_case=test_cases[i],
                    status=result['status'],
                    execution_time=result['execution_time'],
                    memory_used=result['memory_used'],
                    actual_output=result['actual_output'],
                    error_message=result['error_message']
                )

class TestCaseManager:
    """Manages test cases for problems"""
    
    @staticmethod
    def create_sample_test_cases():
        """Create sample test cases for demonstration"""
        problems = Problem.objects.all()
        
        # Sample test cases for different problem types
        sample_cases = {
            "Two Sum": [
                {
                    'input': "4 2 7 11 15\n9",
                    'output': "0 1",
                    'is_sample': True
                },
                {
                    'input': "3 3 2 4\n6",
                    'output': "1 2",
                    'is_sample': True
                },
                {
                    'input': "2 3 3\n6",
                    'output': "0 1",
                    'is_sample': False
                }
            ],
            "Add Two Numbers": [
                {
                    'input': "2 4 3\n5 6 4",
                    'output': "7 0 8",
                    'is_sample': True
                },
                {
                    'input': "1\n1",
                    'output': "2",
                    'is_sample': True
                },
                {
                    'input': "9 9 9 9 9 9 9\n9 9 9 9",
                    'output': "8 9 9 9 0 0 0 1",
                    'is_sample': False
                }
            ],
            "Longest Substring Without Repeating Characters": [
                {
                    'input': "abcabcbb",
                    'output': "3",
                    'is_sample': True
                },
                {
                    'input': "bbbbb",
                    'output': "1",
                    'is_sample': True
                },
                {
                    'input': "pwwkew",
                    'output': "3",
                    'is_sample': True
                }
            ]
        }
        
        for problem in problems:
            if problem.title in sample_cases:
                print(f"Creating test cases for {problem.title}")
                for i, case in enumerate(sample_cases[problem.title]):
                    # Ensure input format is correct
                    input_data = case['input']
                    if not input_data.endswith('\n'):
                        input_data += '\n'
                    
                    test_case, created = TestCase.objects.get_or_create(
                        problem=problem,
                        input_data=input_data,
                        expected_output=case['output'],
                        defaults={
                            'is_sample': case['is_sample'],
                            'order': i
                        }
                    )
                    if created:
                        print(f"Created test case {i+1} for {problem.title}")
                    else:
                        print(f"Test case {i+1} already exists for {problem.title}")
    
    @staticmethod
    def test_test_cases():
        """Test the test cases to ensure they work correctly"""
        problems = Problem.objects.all()
        
        for problem in problems:
            print(f"\n=== Testing problem: {problem.title} ===")
            test_cases = problem.test_cases.all()
            
            for i, test_case in enumerate(test_cases):
                print(f"\nTest Case {i+1}:")
                print(f"Input: '{test_case.input_data}'")
                print(f"Expected: '{test_case.expected_output}'")
                print(f"Is Sample: {test_case.is_sample}")
                
                # Test with a simple Python solution
                if problem.title == "Two Sum":
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
                    
                    compiler = CodeCompiler()
                    result = compiler.compile_and_run(test_code, "python", test_case.input_data)
                    print(f"Compiler result: {result}")
                    print(f"Actual output: '{result.get('output', '')}'")
                    print(f"Error: '{result.get('error', '')}'")
                    compiler.cleanup() 