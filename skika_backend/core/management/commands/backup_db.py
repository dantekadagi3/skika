from django.core.management.base import BaseCommand
import subprocess
import time

class Command(BaseCommand):
    help = 'Backup the PostgreSQL database'

    def handle(self, *args, **options):
        with transaction.atomic():  # Ensure atomic backup process
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = f'backup_{timestamp}.sql'
            subprocess.run([
                'pg_dump', '-U', 'your_user', 'skika_db', '-f', backup_file
            ])
            self.stdout.write(self.style.SUCCESS(f'Backup completed: {backup_file}'))