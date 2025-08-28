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


class Place(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
