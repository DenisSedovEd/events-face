from django.urls import path

from .views import EventListView, RegistrationEventView

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("register/", RegistrationEventView.as_view(), name="event-register"),
]
