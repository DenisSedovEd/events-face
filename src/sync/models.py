from django.db import models


class SyncEventResult(models.Model):
    SYNC_TYPE_CHOICES = (
        ("date", "By Date"),
        ("all", "All"),
    )
    sync_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата синхронизации",
    )
    target_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Синхронизируемая дата",
    )
    sync_type = models.CharField(
        max_length=10,
        choices=SYNC_TYPE_CHOICES,
        verbose_name="Тип синхронизации",
    )
    new_events = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество новых событий",
    )
    updated_events = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество обновленных событий",
    )

    def __str__(self):
        return f"Синхронизация от {self.sync_date}, тип - {self.sync_type}"
