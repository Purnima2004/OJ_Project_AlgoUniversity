from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from auth_app.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile objects for all users who do not have one'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        
        if not users_without_profiles.exists():
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles!')
            )
            return
        
        created_count = 0
        for user in users_without_profiles:
            UserProfile.objects.create(
                user=user,
                score=0,
                rank=0
            )
            created_count += 1
            self.stdout.write(f'Created profile for user: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} user profiles!')
        ) 