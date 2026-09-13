from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds the database with sample"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Loading fixtures..."))

        try:
            call_command("loaddata", "data.json")
            self.stdout.write(self.style.SUCCESS("Successfully seeded the database."))
        except Exception as e:  # noqa: BLE001
            self.stdout.write(
                self.style.ERROR(f"Error occurred while loading fixtures: {e}")
            )
