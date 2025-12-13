from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Ensure media directories exist with proper permissions'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        
        # Create subdirectories
        directories = [
            os.path.join(media_root, 'articles', 'pdfs'),
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, mode=0o755, exist_ok=True)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created/verified directory: {directory}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to create directory {directory}: {e}')
                )
        
        self.stdout.write(self.style.SUCCESS('Media directories setup complete'))
