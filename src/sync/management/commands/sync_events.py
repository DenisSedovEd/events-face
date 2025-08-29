from datetime import datetime, timedelta

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from events.models import Event, Place
from sync.models import SyncEventResult

API_URL = "https://events.k3scluster.tech/api/events/"


def parse_event(event_data):
    # предположим что есть вот такие поля
    return {
        "id": event_data.get("id"),
        "name": event_data.get("name"),
        "date": event_data.get("date"),
        "status": event_data.get("status"),
        "venue": event_data.get("venue"),
    }


class Command(BaseCommand):
    help = "Синхронизация ивентов с API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date", type=str, help="Дата для синхронизации (формат YYYY-MM-DD)"
        )
        parser.add_argument(
            "--all", action="store_true", help="Синхронизировать все ивенты"
        )

    def handle(self, *args, **options):
        sync_type = "all" if options["all"] else "date"
        target_date = None

        if options["all"]:
            url = API_URL
        else:
            if options["date"]:
                try:
                    target_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
                except ValueError:
                    self.stderr.write(
                        self.style.ERROR(
                            "Некорректный формат даты (должен быть YYYY-MM-DD)"
                        )
                    )
                    return
            else:
                target_date = (timezone.now() - timedelta(days=1)).date()
            url = f"{API_URL}?changed_at={target_date}"

        self.stdout.write(f"Запрос: {url}")

        resp = requests.get(url)
        if resp.status_code != 200:
            self.stderr.write(
                self.style.ERROR(f"Ошибка запроса к провайдеру: {resp.status_code}")
            )
            return

        events = resp.json()
        new_count = 0
        updated_count = 0

        with transaction.atomic():
            for event in events:
                ext_id = event["id"]
                defaults = {
                    "name": event["name"],
                    "date": event["date"],
                    "status": event["status"],
                }
                # venue обработка, если есть
                venue_name = event.get("venue")
                if venue_name:
                    venue_obj, _ = Place.objects.get_or_create(name=venue_name)
                    defaults["venue"] = venue_obj
                else:
                    defaults["venue"] = None

                obj, created = Event.objects.update_or_create(
                    id=ext_id, defaults=defaults
                )
                if created:
                    new_count += 1
                else:
                    updated_count += 1

            SyncEventResult.objects.create(
                target_date=target_date,
                sync_type=sync_type,
                new_events=new_count,
                updated_events=updated_count,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Синхронизация завершена. Новых: {new_count}, обновлено: {updated_count}"
            )
        )
