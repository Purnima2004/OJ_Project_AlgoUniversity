from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auth_app.models import Problem, Contest, ConceptOfDay, User, UserProfile
from django.contrib.auth.models import User as AuthUser

class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample problems
        problems_data = [
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
                'difficulty': 'Easy',
                'test_cases': '[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6',
                'examples': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].',
                'constraints': '2 <= nums.length <= 104\n-109 <= nums[i] <= 109\n-109 <= target <= 109'
            },
            {
                'title': 'Add Two Numbers',
                'description': 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit.',
                'difficulty': 'Medium',
                'test_cases': '[2,4,3]\n[5,6,4]\n[0]\n[0]\n[9,9,9,9,9,9,9]\n[9,9,9,9]',
                'examples': 'Input: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [7,0,8]\nExplanation: 342 + 465 = 807.',
                'constraints': 'The number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros.'
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'difficulty': 'Medium',
                'test_cases': '"abcabcbb"\n"bbbbb"\n"pwwkew"',
                'examples': 'Input: s = "abcabcbb"\nOutput: 3\nExplanation: The answer is "abc", with the length of 3.',
                'constraints': '0 <= s.length <= 5 * 104\ns consists of English letters, digits, symbols and spaces.'
            },
            {
                'title': 'Median of Two Sorted Arrays',
                'description': 'Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.',
                'difficulty': 'Hard',
                'test_cases': '[1,3]\n[2]\n[1,2]\n[3,4]',
                'examples': 'Input: nums1 = [1,3], nums2 = [2]\nOutput: 2.00000\nExplanation: merged array = [1,2,3] and median is 2.',
                'constraints': 'nums1.length == m\nnums2.length == n\n0 <= m <= 1000\n0 <= n <= 1000\n1 <= m + n <= 2000\n-106 <= nums1[i], nums2[i] <= 106'
            }
        ]
        
        for problem_data in problems_data:
            problem, created = Problem.objects.get_or_create(
                title=problem_data['title'],
                defaults=problem_data
            )
            if created:
                self.stdout.write(f'Created problem: {problem.title}')
        
        # Create sample contests
        contests_data = [
            {
                'title': 'Weekly Contest 1',
                'description': 'Join our first weekly contest featuring array and string problems. Perfect for beginners!',
                'start_date': timezone.now() + timedelta(days=1),
                'end_date': timezone.now() + timedelta(days=1, hours=2),
                'is_active': True
            },
            {
                'title': 'Algorithm Master Challenge',
                'description': 'Advanced algorithmic problems for experienced programmers. Test your skills!',
                'start_date': timezone.now() + timedelta(days=3),
                'end_date': timezone.now() + timedelta(days=3, hours=3),
                'is_active': True
            },
            {
                'title': 'Beginner Friendly Contest',
                'description': 'A contest designed specifically for beginners with easy to medium difficulty problems.',
                'start_date': timezone.now() + timedelta(days=7),
                'end_date': timezone.now() + timedelta(days=7, hours=2),
                'is_active': True
            }
        ]
        
        for contest_data in contests_data:
            contest, created = Contest.objects.get_or_create(
                title=contest_data['title'],
                defaults=contest_data
            )
            if created:
                # Add some problems to the contest
                problems = Problem.objects.all()[:3]
                contest.problems.set(problems)
                self.stdout.write(f'Created contest: {contest.title}')
        
        # Create concept of the day
        concept_data = {
            'title': 'Dynamic Programming',
            'description': 'Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. It is applicable when the subproblems are not independent, that is, when subproblems share subsubproblems.',
            'concept_type': 'DP',
            'date': timezone.now().date(),
            'example_code': 'def fibonacci(n):\n    if n <= 1:\n        return n\n    dp = [0] * (n + 1)\n    dp[1] = 1\n    for i in range(2, n + 1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]'
        }
        
        concept, created = ConceptOfDay.objects.get_or_create(
            date=concept_data['date'],
            defaults=concept_data
        )
        if created:
            self.stdout.write(f'Created concept of the day: {concept.title}')
        
        # Create a sample user if none exists
        if not AuthUser.objects.filter(username='testuser').exists():
            user = AuthUser.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            UserProfile.objects.create(
                user=user,
                score=0,
                rank=1
            )
            self.stdout.write('Created test user: testuser (password: testpass123)')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!')) 