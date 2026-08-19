from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    """Модель полезной или приятной привычки."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dependent_habits",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность в днях")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveSmallIntegerField(verbose_name="Время выполнения в секундах")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    last_notification_date = models.DateField(blank=True, null=True, verbose_name="Последняя дата напоминания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def __str__(self):
        return f"{self.user} - {self.action}"

    def clean(self):
        """Проверяет бизнес-правила привычки."""
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указывать и вознаграждение, и связанную привычку.")

        if self.execution_time > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

    def save(self, *args, **kwargs):
        """Перед сохранением прогоняет валидацию модели."""
        self.full_clean()
        return super().save(*args, **kwargs)
