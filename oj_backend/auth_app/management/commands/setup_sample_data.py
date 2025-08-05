from django.core.management.base import BaseCommand
from auth_app.models import Problem, TestCase
from auth_app.oj_system import TestCaseManager

class Command(BaseCommand):
    help = 'Create sample problems and test cases for the OJ system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample problems and test cases...')
        
        # Create sample problems
        problems_data = [
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
                'difficulty': 'Easy',
                'examples': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]\nExplanation: Because nums[1] + nums[2] == 6, we return [1, 2].',
                'constraints': '2 <= nums.length <= 104\n-109 <= nums[i] <= 109\n-109 <= target <= 109\nOnly one valid answer exists.',
                'time_limit': 1000,
                'memory_limit': 256
            },
            {
                'title': 'Add Two Numbers',
                'description': 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.',
                'difficulty': 'Medium',
                'examples': 'Input: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [7,0,8]\nExplanation: 342 + 465 = 807.\n\nInput: l1 = [0], l2 = [0]\nOutput: [0]\nExplanation: 0 + 0 = 0.',
                'constraints': 'The number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros.',
                'time_limit': 1000,
                'memory_limit': 256
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'difficulty': 'Medium',
                'examples': 'Input: s = "abcabcbb"\nOutput: 3\nExplanation: The answer is "abc", with the length of 3.\n\nInput: s = "bbbbb"\nOutput: 1\nExplanation: The answer is "b", with the length of 1.\n\nInput: s = "pwwkew"\nOutput: 3\nExplanation: The answer is "wke", with the length of 3.',
                'constraints': '0 <= s.length <= 5 * 104\ns consists of English letters, digits, symbols and spaces.',
                'time_limit': 1000,
                'memory_limit': 256
            },
            {
                'title': 'Reverse String',
                'description': 'Write a function that reverses a string. The input string is given as an array of characters s.\n\nYou must do this by modifying the input array in-place with O(1) extra memory.',
                'difficulty': 'Easy',
                'examples': 'Input: s = ["h","e","l","l","o"]\nOutput: ["o","l","l","e","h"]\n\nInput: s = ["H","a","n","n","a","h"]\nOutput: ["h","a","n","n","a","H"]',
                'constraints': '1 <= s.length <= 105\ns[i] is a printable ascii character.',
                'time_limit': 1000,
                'memory_limit': 256
            },
            {
                'title': 'Valid Parentheses',
                'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.',
                'difficulty': 'Easy',
                'examples': 'Input: s = "()"\nOutput: true\n\nInput: s = "()[]{}"\nOutput: true\n\nInput: s = "(]"\nOutput: false',
                'constraints': '1 <= s.length <= 104\ns consists of parentheses only \'()[]{}\'',
                'time_limit': 1000,
                'memory_limit': 256
            }
        ]
        
        for data in problems_data:
            problem, created = Problem.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created problem: {problem.title}')
            else:
                self.stdout.write(f'Problem already exists: {problem.title}')
        
        # Create sample test cases
        test_cases_data = {
            'Two Sum': [
                {
                    'input_data': '4\n2 7 11 15\n9',
                    'expected_output': '0 1',
                    'is_sample': True,
                    'order': 0
                },
                {
                    'input_data': '3\n3 2 4\n6',
                    'expected_output': '1 2',
                    'is_sample': True,
                    'order': 1
                },
                {
                    'input_data': '2\n3 3\n6',
                    'expected_output': '0 1',
                    'is_sample': False,
                    'order': 2
                }
            ],
            'Add Two Numbers': [
                {
                    'input_data': '2 4 3\n5 6 4',
                    'expected_output': '7 0 8',
                    'is_sample': True,
                    'order': 0
                },
                {
                    'input_data': '1\n1',
                    'expected_output': '2',
                    'is_sample': True,
                    'order': 1
                },
                {
                    'input_data': '9 9 9 9 9 9 9\n9 9 9 9',
                    'expected_output': '8 9 9 9 0 0 0 1',
                    'is_sample': False,
                    'order': 2
                }
            ],
            'Longest Substring Without Repeating Characters': [
                {
                    'input_data': 'abcabcbb',
                    'expected_output': '3',
                    'is_sample': True,
                    'order': 0
                },
                {
                    'input_data': 'bbbbb',
                    'expected_output': '1',
                    'is_sample': True,
                    'order': 1
                },
                {
                    'input_data': 'pwwkew',
                    'expected_output': '3',
                    'is_sample': True,
                    'order': 2
                }
            ],
            'Reverse String': [
                {
                    'input_data': 'hello',
                    'expected_output': 'olleh',
                    'is_sample': True,
                    'order': 0
                },
                {
                    'input_data': 'world',
                    'expected_output': 'dlrow',
                    'is_sample': True,
                    'order': 1
                },
                {
                    'input_data': 'a',
                    'expected_output': 'a',
                    'is_sample': False,
                    'order': 2
                }
            ],
            'Valid Parentheses': [
                {
                    'input_data': '()',
                    'expected_output': 'true',
                    'is_sample': True,
                    'order': 0
                },
                {
                    'input_data': '()[]{}',
                    'expected_output': 'true',
                    'is_sample': True,
                    'order': 1
                },
                {
                    'input_data': '(]',
                    'expected_output': 'false',
                    'is_sample': True,
                    'order': 2
                }
            ]
        }
        
        for problem_title, cases in test_cases_data.items():
            try:
                problem = Problem.objects.get(title=problem_title)
                for case in cases:
                    test_case, created = TestCase.objects.get_or_create(
                        problem=problem,
                        input_data=case['input_data'],
                        expected_output=case['expected_output'],
                        defaults={
                            'is_sample': case['is_sample'],
                            'order': case['order']
                        }
                    )
                    if created:
                        self.stdout.write(f'Created test case for {problem_title}')
            except Problem.DoesNotExist:
                self.stdout.write(f'Problem not found: {problem_title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!')) 