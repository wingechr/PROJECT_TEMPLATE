from django.core.management.base import BaseCommand, CommandError


class ExampleCommand(BaseCommand):
    def handle(self, *args, **options):
        raise CommandError("Not implemented")
