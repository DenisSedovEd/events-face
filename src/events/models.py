from django.db import models


class Event(models.Model):
    class StatusEvent(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(
        choices=StatusEvent.choices,
        default=StatusEvent.OPEN,
    )
    place = models.ForeignKey(
        "Place",
        on_delete=models.PROTECT,
    )


class Place(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
