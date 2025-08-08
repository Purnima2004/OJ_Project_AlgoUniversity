from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from auth_app.models import Contest, Problem

class Command(BaseCommand):
    help = 'Update existing contests with different problems and create active contest until August 15th'

    def handle(self, *args, **options):
        # Get contest-specific problems (those with "Contest" in title)
        contest_problems = list(Problem.objects.filter(title__icontains='Contest'))
        
        # Get regular problems (those without "Contest" in title)
        regular_problems = list(Problem.objects.exclude(title__icontains='Contest'))
        
        # Use contest problems if available, otherwise use regular problems
        problems = contest_problems if contest_problems else regular_problems
        
        if len(problems) < 6:
            self.stdout.write(
                self.style.WARNING('Need at least 6 problems to create diverse contests. Please create contest problems first using: python manage.py create_contest_problems')
            )
            return
        
        # Clear existing contests
        Contest.objects.all().delete()
        self.stdout.write('Cleared existing contests')
        
        now = timezone.now()
        
        # Contest 1: Active contest until August 15th, 2025
        august_15 = datetime(2025, 8, 15, 23, 59, 59, tzinfo=timezone.get_current_timezone())
        contest1, created1 = Contest.objects.get_or_create(
            title="Summer Coding Championship 2025",
            defaults={
                'description': 'Join the ultimate summer coding challenge! Solve problems, compete with coders worldwide, and win recognition. Open until August 15th, 2025.',
                'start_date': now - timedelta(days=1),  # Started yesterday
                'end_date': august_15,
                'is_active': True
            }
        )
        
        if created1:
            # Add problems 0, 1, 2 to contest 1
            for problem in problems[:3]:
                contest1.problems.add(problem)
            self.stdout.write(f'Created active contest: {contest1.title} (until August 15th)')
        else:
            self.stdout.write(f'Contest already exists: {contest1.title}')
        
        # Contest 2: Upcoming contest
        contest2, created2 = Contest.objects.get_or_create(
            title="Advanced Algorithms Masterclass",
            defaults={
                'description': 'Advanced algorithms contest featuring complex problems. Only for experienced coders!',
                'start_date': now + timedelta(days=3),
                'end_date': now + timedelta(days=3, hours=4),
                'is_active': True
            }
        )
        
        if created2:
            # Add problems 3, 4, 5 to contest 2 (different from contest 1)
            for problem in problems[3:6]:
                contest2.problems.add(problem)
            self.stdout.write(f'Created upcoming contest: {contest2.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest2.title}')
        
        # Contest 3: Future contest
        contest3, created3 = Contest.objects.get_or_create(
            title="Data Structures Challenge",
            defaults={
                'description': 'Master data structures with this comprehensive challenge. Perfect for intermediate coders!',
                'start_date': now + timedelta(days=7),
                'end_date': now + timedelta(days=7, hours=5),
                'is_active': True
            }
        )
        
        if created3:
            # Add problems 0, 2, 4 to contest 3 (different combination)
            contest3.problems.add(problems[0])
            contest3.problems.add(problems[2])
            contest3.problems.add(problems[4])
            self.stdout.write(f'Created future contest: {contest3.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest3.title}')
        
        # Contest 4: Ended contest
        contest4, created4 = Contest.objects.get_or_create(
            title="Beginner Friendly Contest",
            defaults={
                'description': 'A beginner-friendly contest with easy problems. Perfect for new coders!',
                'start_date': now - timedelta(days=14),
                'end_date': now - timedelta(days=13, hours=21),
                'is_active': True
            }
        )
        
        if created4:
            # Add problems 1, 3, 5 to contest 4 (different combination)
            contest4.problems.add(problems[1])
            contest4.problems.add(problems[3])
            contest4.problems.add(problems[5])
            self.stdout.write(f'Created ended contest: {contest4.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest4.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully updated contests with diverse problem sets!')
        )
        
        # Print contest details
        self.stdout.write('\nContest Details:')
        for contest in Contest.objects.all():
            self.stdout.write(f'- {contest.title}: {contest.problems.count()} problems')
            for problem in contest.problems.all():
                self.stdout.write(f'  * {problem.title} ({problem.difficulty})') 