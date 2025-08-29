from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    class StatusEvent(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=100, verbose_name="Название")
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        choices=StatusEvent.choices,
        default=StatusEvent.OPEN,
        verbose_name="Статус мероприятия",
    )
    place = models.ForeignKey(
        "Place", on_delete=models.PROTECT, verbose_name="Место проведения"
    )
    registration_deadline = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.event_time and not self.registration_deadline:
            self.registration_deadline = self.event_time - timedelta(hours=2)
        super().save(*args, **kwargs)


class Place(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
    )
    registration_at = models.DateTimeField(
        auto_now_add=True,
    )
    notification_send = models.BooleanField(
        default=False,
    )

    class Meta:
        unique_together = ("user", "event")
