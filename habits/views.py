"""Представления API для привычек."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Список привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related("user", "related_habit")


class PublicHabitListAPIView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).select_related("user", "related_habit")


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр одной привычки владельца."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related("user", "related_habit")


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки владельцем."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).select_related("user", "related_habit")


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки владельцем."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
