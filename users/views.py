"""Представления для пользователей и JWT."""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import MyTokenObtainPairSerializer, UserRegisterSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """JWT логин по email и паролю."""

    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    """Обновление JWT токена."""


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация пользователя."""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """Список из одного текущего пользователя."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
