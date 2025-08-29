from celery.utils.time import timezone
from django.core.management import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = "Delete old events, ended more that 7 days ago."

    def handle(self, *args, **kwargs):
        now = timezone.now()
        cutoff = now - timezone.timedelta(days=7)
        deleted, _ = Event.objects.all().filter(date__lt=cutoff).delete()
        self.stdout.write(f"Deleted {deleted} events")
