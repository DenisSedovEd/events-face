from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # serializer = RegisterSerializer(data=request.data)
        return Response(
            {
                "username": "",
                "password": "",
            }
        )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(
                username=serializer.validated_data["username"]
            ).exists():
                return Response({"error": "Username already exists"}, status=400)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User created successfully",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status=201,
            )
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # serializer = RegisterSerializer(data=request.data)
        return Response(
            {
                "username": "",
                "password": "",
            }
        )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }
            )
        else:
            return Response({"error": "Invalid username or password"}, status=401)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({"access_token": response.data["access"]})
        return Response({"error": "Invalid or expired refresh token"}, status=401)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=205)
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=400)
