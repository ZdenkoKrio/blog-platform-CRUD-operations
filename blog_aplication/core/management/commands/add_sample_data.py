from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run multiple custom commands from different apps in sequence'

    def handle(self, *args, **kwargs):
        commands = [
            'add_sample_users',
            'add_sample_categories',
            'add_sample_posts',
            'add_sample_comments',
        ]

        for command in commands:
            try:
                self.stdout.write(self.style.SUCCESS(f'Running command: {command}'))
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f'Successfully ran command: {command}'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'Error running command {command}: {e}'))