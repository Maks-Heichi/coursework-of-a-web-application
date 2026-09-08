"""Пагинация для API привычек."""

from rest_framework.pagination import LimitOffsetPagination


class HabitPagination(LimitOffsetPagination):
    """Пагинация по 5 привычек на страницу."""

    default_limit = 5
    max_limit = 50
