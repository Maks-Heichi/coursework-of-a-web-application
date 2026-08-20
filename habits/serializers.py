"""Сериализаторы для привычек."""

from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки с бизнес-валидацией."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        """Проверяет правила валидации перед сохранением."""
        related_habit = attrs.get("related_habit", getattr(self.instance, "related_habit", None))
        reward = attrs.get("reward", getattr(self.instance, "reward", None))
        execution_time = attrs.get("execution_time", getattr(self.instance, "execution_time", None))
        periodicity = attrs.get("periodicity", getattr(self.instance, "periodicity", 1))
        is_pleasant = attrs.get("is_pleasant", getattr(self.instance, "is_pleasant", False))
        request = self.context.get("request")
        owner = request.user if request else getattr(self.instance, "user", None)

        if reward and related_habit:
            raise serializers.ValidationError("Нельзя одновременно указывать и вознаграждение, и связанную привычку.")

        if execution_time and execution_time > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд.")

        if periodicity is not None and (periodicity < 1 or periodicity > 7):
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("В связанные привычки могут попадать только приятные привычки.")

        if self.instance and related_habit and related_habit.pk == self.instance.pk:
            raise serializers.ValidationError("Нельзя связать привычку саму с собой.")

        if related_habit and owner and related_habit.user != owner:
            raise serializers.ValidationError("Связанная привычка должна принадлежать текущему пользователю.")

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        return attrs
