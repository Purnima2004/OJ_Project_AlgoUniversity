from django.core.management.base import BaseCommand
from auth_app.models import Problem, TestCase
import json

class Command(BaseCommand):
    help = 'Create separate contest problems that are different from regular problems'

    def handle(self, *args, **options):
        # Contest-specific problems (different from regular problems)
        contest_problems = [
            {
                'title': 'Contest Two Sum',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
                'difficulty': 'Easy',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].',
                    'Input: nums = [3,2,4], target = 6\nOutput: [1,2]\nExplanation: Because nums[1] + nums[2] == 6, we return [1, 2].',
                    'Input: nums = [3,3], target = 6\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 6, we return [0, 1].'
                ],
                'constraints': [
                    '2 <= nums.length <= 10^4',
                    '-10^9 <= nums[i] <= 10^9',
                    '-10^9 <= target <= 10^9',
                    'Only one valid answer exists.'
                ],
                'test_cases': [
                    {'input': '4\n2 7 11 15\n9', 'output': '0 1', 'is_sample': True},
                    {'input': '3\n3 2 4\n6', 'output': '1 2', 'is_sample': True},
                    {'input': '2\n3 3\n6', 'output': '0 1', 'is_sample': True},
                    {'input': '5\n1 2 3 4 5\n9', 'output': '3 4', 'is_sample': False},
                    {'input': '6\n10 20 30 40 50 60\n70', 'output': '0 5', 'is_sample': False},
                ]
            },
            {
                'title': 'Contest Palindrome Check',
                'description': 'Given a string s, return true if it is a palindrome, or false otherwise.\n\nA phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.',
                'difficulty': 'Easy',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: s = "A man, a plan, a canal: Panama"\nOutput: true\nExplanation: "amanaplanacanalpanama" is a palindrome.',
                    'Input: s = "race a car"\nOutput: false\nExplanation: "raceacar" is not a palindrome.',
                    'Input: s = " "\nOutput: true\nExplanation: s is an empty string "" after removing non-alphanumeric characters. Since an empty string reads the same forward and backward, it is a palindrome.'
                ],
                'constraints': [
                    '1 <= s.length <= 2 * 10^5',
                    's consists only of printable ASCII characters.'
                ],
                'test_cases': [
                    {'input': 'A man, a plan, a canal: Panama', 'output': 'true', 'is_sample': True},
                    {'input': 'race a car', 'output': 'false', 'is_sample': True},
                    {'input': ' ', 'output': 'true', 'is_sample': True},
                    {'input': 'Was it a car or a cat I saw?', 'output': 'true', 'is_sample': False},
                    {'input': 'hello world', 'output': 'false', 'is_sample': False},
                ]
            },
            {
                'title': 'Contest Maximum Subarray',
                'description': 'Given an integer array nums, find the subarray with the largest sum, and return its sum.\n\nA subarray is a contiguous non-empty sequence of elements within an array.',
                'difficulty': 'Medium',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\nExplanation: The subarray [4,-1,2,1] has the largest sum 6.',
                    'Input: nums = [1]\nOutput: 1\nExplanation: The subarray [1] has the largest sum 1.',
                    'Input: nums = [5,4,-1,7,8]\nOutput: 23\nExplanation: The subarray [5,4,-1,7,8] has the largest sum 23.'
                ],
                'constraints': [
                    '1 <= nums.length <= 10^5',
                    '-10^4 <= nums[i] <= 10^4'
                ],
                'test_cases': [
                    {'input': '9\n-2 1 -3 4 -1 2 1 -5 4', 'output': '6', 'is_sample': True},
                    {'input': '1\n1', 'output': '1', 'is_sample': True},
                    {'input': '5\n5 4 -1 7 8', 'output': '23', 'is_sample': True},
                    {'input': '4\n-1 -2 -3 -4', 'output': '-1', 'is_sample': False},
                    {'input': '6\n1 2 3 4 5 6', 'output': '21', 'is_sample': False},
                ]
            },
            {
                'title': 'Contest Valid Parentheses',
                'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.',
                'difficulty': 'Easy',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: s = "()"\nOutput: true',
                    'Input: s = "()[]{}"\nOutput: true',
                    'Input: s = "(]"\nOutput: false'
                ],
                'constraints': [
                    '1 <= s.length <= 10^4',
                    's consists of parentheses only \'()[]{}\''
                ],
                'test_cases': [
                    {'input': '()', 'output': 'true', 'is_sample': True},
                    {'input': '()[]{}', 'output': 'true', 'is_sample': True},
                    {'input': '(]', 'output': 'false', 'is_sample': True},
                    {'input': '([)]', 'output': 'false', 'is_sample': False},
                    {'input': '{[]}', 'output': 'true', 'is_sample': False},
                ]
            },
            {
                'title': 'Contest Binary Search',
                'description': 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.',
                'difficulty': 'Easy',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: nums = [-1,0,3,5,9,12], target = 9\nOutput: 4\nExplanation: 9 exists in nums and its index is 4',
                    'Input: nums = [-1,0,3,5,9,12], target = 2\nOutput: -1\nExplanation: 2 does not exist in nums so return -1'
                ],
                'constraints': [
                    '1 <= nums.length <= 10^4',
                    '-10^4 < nums[i], target < 10^4',
                    'All the integers in nums are unique.',
                    'nums is sorted in ascending order.'
                ],
                'test_cases': [
                    {'input': '6\n-1 0 3 5 9 12\n9', 'output': '4', 'is_sample': True},
                    {'input': '6\n-1 0 3 5 9 12\n2', 'output': '-1', 'is_sample': True},
                    {'input': '5\n1 2 3 4 5\n3', 'output': '2', 'is_sample': False},
                    {'input': '4\n10 20 30 40\n50', 'output': '-1', 'is_sample': False},
                ]
            },
            {
                'title': 'Contest Remove Duplicates',
                'description': 'Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.\n\nConsider the number of unique elements of nums to be k, to get accepted, you need to do the following things:\n1. Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.\n2. Return k.',
                'difficulty': 'Easy',
                'time_limit': 1000,
                'memory_limit': 128,
                'examples': [
                    'Input: nums = [1,1,2]\nOutput: 2, nums = [1,2,_]\nExplanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively. It does not matter what you leave beyond the returned k (hence they are underscores).',
                    'Input: nums = [0,0,1,1,1,2,2,3,3,4]\nOutput: 5, nums = [0,1,2,3,4,_,_,_,_,_]\nExplanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively. It does not matter what you leave beyond the returned k (hence they are underscores).'
                ],
                'constraints': [
                    '1 <= nums.length <= 3 * 10^4',
                    '-100 <= nums[i] <= 100',
                    'nums is sorted in non-decreasing order.'
                ],
                'test_cases': [
                    {'input': '3\n1 1 2', 'output': '2', 'is_sample': True},
                    {'input': '10\n0 0 1 1 1 2 2 3 3 4', 'output': '5', 'is_sample': True},
                    {'input': '5\n1 2 3 4 5', 'output': '5', 'is_sample': False},
                    {'input': '4\n1 1 1 1', 'output': '1', 'is_sample': False},
                ]
            }
        ]
        
        # Clear existing contest problems (those with "Contest" in title)
        existing_contest_problems = Problem.objects.filter(title__icontains='Contest')
        if existing_contest_problems.exists():
            self.stdout.write(f'Deleting {existing_contest_problems.count()} existing contest problems...')
            existing_contest_problems.delete()
        
        created_count = 0
        
        for problem_data in contest_problems:
            # Create the problem
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                time_limit=problem_data['time_limit'],
                memory_limit=problem_data['memory_limit'],
                examples=json.dumps(problem_data['examples']),
                constraints=json.dumps(problem_data['constraints'])
            )
            
            # Create test cases
            for test_case_data in problem_data['test_cases']:
                TestCase.objects.create(
                    problem=problem,
                    input_data=test_case_data['input'],
                    expected_output=test_case_data['output'],
                    is_sample=test_case_data['is_sample']
                )
            
            created_count += 1
            self.stdout.write(f'Created contest problem: {problem.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} contest problems!')
        )
        
        # Print summary
        self.stdout.write('\nContest Problems Summary:')
        contest_problems = Problem.objects.filter(title__icontains='Contest')
        for problem in contest_problems:
            test_cases_count = problem.test_cases.count()
            sample_cases_count = problem.test_cases.filter(is_sample=True).count()
            self.stdout.write(f'- {problem.title} ({problem.difficulty}): {test_cases_count} test cases ({sample_cases_count} sample)') 