from django.core.management.base import BaseCommand
from auth_app.models import ContestParticipation

class Command(BaseCommand):
    help = 'Clean up old inactive contest participations'

    def handle(self, *args, **options):
        # Get all inactive participations
        inactive_participations = ContestParticipation.objects.filter(is_active=False)
        
        if inactive_participations.exists():
            count = inactive_participations.count()
            self.stdout.write(f'Found {count} inactive participations to clean up...')
            
            # Delete inactive participations
            inactive_participations.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cleaned up {count} inactive participations!')
            )
        else:
            self.stdout.write('No inactive participations found to clean up.')
        
        # Also check for participations in ended contests
        from django.utils import timezone
        ended_contests_participations = ContestParticipation.objects.filter(
            contest__end_date__lt=timezone.now(),
            is_active=True
        )
        
        if ended_contests_participations.exists():
            count = ended_contests_participations.count()
            self.stdout.write(f'Found {count} active participations in ended contests...')
            
            # Mark them as inactive
            ended_contests_participations.update(is_active=False)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully marked {count} participations as inactive!')
            )
        else:
            self.stdout.write('No active participations in ended contests found.')
