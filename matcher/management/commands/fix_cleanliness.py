from django.core.management.base import BaseCommand
from matcher.models import UserProfile

class Command(BaseCommand):
    help = 'Fix string cleanliness values in UserProfile'

    def handle(self, *args, **options):
        count_fixed = 0
        count_failed = 0

        for profile in UserProfile.objects.all():
            if isinstance(profile.cleanliness, str):
                try:
                    profile.cleanliness = int(profile.cleanliness)
                    profile.save()
                    self.stdout.write(self.style.SUCCESS(f'✅ Fixed: {profile.email}'))
                    count_fixed += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Could not fix: {profile.email} — {profile.cleanliness}'))
                    count_failed += 1

        self.stdout.write(self.style.WARNING(f'\n✅ Fixed: {count_fixed}'))
        self.stdout.write(self.style.WARNING(f'❌ Failed: {count_failed}'))
