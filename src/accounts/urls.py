from django.urls import path

from .views import CustomTokenRefreshView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path("register", RegisterView.as_view(), name="auth_register"),
    path("login", LoginView.as_view(), name="auth_login"),
    path("token/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout", LogoutView.as_view(), name="auth_logout"),
]
