from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auth_app.models import Contest, Problem

class Command(BaseCommand):
    help = 'Create sample contests for testing'

    def handle(self, *args, **options):
        # Get existing problems
        problems = Problem.objects.all()
        
        if not problems.exists():
            self.stdout.write(
                self.style.WARNING('No problems found. Please create problems first.')
            )
            return
        
        # Create sample contests
        now = timezone.now()
        
        # Contest 1: Currently running
        contest1, created1 = Contest.objects.get_or_create(
            title="Weekly Coding Challenge",
            defaults={
                'description': 'A weekly coding challenge with problems of varying difficulty. Test your skills and compete with others!',
                'start_date': now - timedelta(hours=2),
                'end_date': now + timedelta(hours=22),
                'is_active': True
            }
        )
        
        if created1:
            # Add problems to contest
            for problem in problems[:3]:  # Add first 3 problems
                contest1.problems.add(problem)
            self.stdout.write(f'Created contest: {contest1.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest1.title}')
        
        # Contest 2: Upcoming
        contest2, created2 = Contest.objects.get_or_create(
            title="Advanced Algorithms Contest",
            defaults={
                'description': 'Advanced algorithms contest featuring complex problems. Only for experienced coders!',
                'start_date': now + timedelta(days=2),
                'end_date': now + timedelta(days=2, hours=3),
                'is_active': True
            }
        )
        
        if created2:
            # Add problems to contest
            for problem in problems:  # Add all problems
                contest2.problems.add(problem)
            self.stdout.write(f'Created contest: {contest2.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest2.title}')
        
        # Contest 3: Ended
        contest3, created3 = Contest.objects.get_or_create(
            title="Beginner Friendly Contest",
            defaults={
                'description': 'A beginner-friendly contest with easy problems. Perfect for new coders!',
                'start_date': now - timedelta(days=7),
                'end_date': now - timedelta(days=6, hours=21),
                'is_active': True
            }
        )
        
        if created3:
            # Add problems to contest
            for problem in problems[:2]:  # Add first 2 problems
                contest3.problems.add(problem)
            self.stdout.write(f'Created contest: {contest3.title}')
        else:
            self.stdout.write(f'Contest already exists: {contest3.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample contests!')
        ) 