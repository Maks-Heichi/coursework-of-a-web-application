from datetime import time

from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    """Тесты API привычек."""

    def setUp(self):
        self.user = User.objects.create_user(email="owner@example.com", password="strongpass123")
        self.other_user = User.objects.create_user(email="other@example.com", password="strongpass123")
        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Выпить воды",
            is_pleasant=True,
            periodicity=1,
            execution_time=60,
            is_public=False,
        )

    def test_create_habit_with_reward_and_related_habit_fails(self):
        """Проверяет запрет на одновременные reward и related_habit."""
        payload = {
            "place": "Парк",
            "time": "09:00:00",
            "action": "Пробежка",
            "is_pleasant": False,
            "related_habit": self.pleasant_habit.pk,
            "periodicity": 1,
            "reward": "Кофе",
            "execution_time": 120,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_with_long_execution_time_fails(self):
        """Проверяет ограничение времени выполнения привычки."""
        payload = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Чтение",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 121,
            "is_public": False,
        }

        response = self.client.post("/habits/create/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_with_zero_periodicity_fails(self):
        """Проверяет запрет periodicity=0."""
        payload = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Чтение",
            "is_pleasant": False,
            "periodicity": 0,
            "execution_time": 60,
            "is_public": False,
        }

        response = self.client.post("/habits/create/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_list_returns_only_current_user_habits(self):
        """Проверяет, что пользователь видит только свои привычки."""
        Habit.objects.create(
            user=self.user,
            place="Офис",
            time=time(11, 0),
            action="Сделать разминку",
            is_pleasant=False,
            periodicity=1,
            execution_time=90,
            is_public=False,
        )
        Habit.objects.create(
            user=self.other_user,
            place="Улица",
            time=time(12, 0),
            action="Прогулка",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
            is_public=True,
        )

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_habit_list_is_paginated_by_five_items(self):
        """Проверяет пагинацию списка привычек по 5 элементов."""
        for index in range(6):
            Habit.objects.create(
                user=self.user,
                place=f"Место {index}",
                time=time(9, 0),
                action=f"Действие {index}",
                is_pleasant=False,
                periodicity=1,
                execution_time=60,
                is_public=False,
            )

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 7)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_public_habit_list_returns_only_public_habits(self):
        """Проверяет список только публичных привычек."""
        Habit.objects.create(
            user=self.user,
            place="Зал",
            time=time(13, 0),
            action="Растяжка",
            is_pleasant=False,
            periodicity=1,
            execution_time=100,
            is_public=False,
        )
        public_habit = Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time=time(14, 0),
            action="Йога",
            is_pleasant=False,
            periodicity=1,
            execution_time=70,
            is_public=True,
        )

        response = self.client.get("/habits/public/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], public_habit.id)

    def test_user_cannot_update_other_users_habit(self):
        """Проверяет запрет на изменение чужой привычки."""
        other_habit = Habit.objects.create(
            user=self.other_user,
            place="Улица",
            time=time(15, 0),
            action="Бег",
            is_pleasant=False,
            periodicity=1,
            execution_time=100,
            is_public=False,
        )

        response = self.client.patch(
            f"/habits/{other_habit.pk}/update/",
            {"action": "Новый текст"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
