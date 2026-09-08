"""Права доступа для профиля пользователя."""

from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    """Разрешает доступ только к собственному профилю."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
