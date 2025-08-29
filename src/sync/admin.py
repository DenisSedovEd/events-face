from django.contrib import admin

from .models import SyncEventResult


@admin.register(SyncEventResult)
class SyncResultAdmin(admin.ModelAdmin):
    list_display = (
        "sync_date",
        "target_date",
        "sync_type",
        "new_events",
        "updated_events",
    )
    list_filter = ("sync_type",)
    search_fields = ("target_date",)
