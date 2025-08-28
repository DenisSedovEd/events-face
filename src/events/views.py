from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .models import Event
from .serializers import EventSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.select_related("place").filter(
        status=Event.StatusEvent.OPEN
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    serializer_class = EventSerializer
    filter_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["date"]
    ordering = ["date"]

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get("name")
        if name:
            qs = qs.filter(name__icontains=name)
        return qs
