from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from .task import async_registration_for_event


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


class RegistrationEventView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = request.data["event"]
        event = Event.objects.get(pk=event_id)
        user = self.request.user

        if event.registration_deadline < timezone.now():
            return Response(
                {
                    "message": "Event is deadline",
                },
                status=400,
            )
        reg, created = Registration.objects.get_or_create(event=event, user=user)
        if not created:
            return Response(
                {
                    "message": "User is already registered",
                },
                status=400,
            )
        async_registration_for_event.delay(reg.id)
        return Response(
            {
                "message": "Registration queued",
            },
            status=202,
        )
