from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):
    """Тесты API пользователей."""

    def test_user_registration(self):
        """Проверяет успешную регистрацию пользователя."""
        payload = {
            "email": "user@example.com",
            "password": "strongpass123",
            "first_name": "Max",
            "last_name": "Test",
            "telegram_chat_id": "123456789",
        }

        response = self.client.post("/users/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_jwt_token_obtain(self):
        """Проверяет получение JWT токена по email и паролю."""
        user = User.objects.create_user(email="jwt@example.com", password="strongpass123")

        response = self.client.post(
            "/token/",
            {"email": user.email, "password": "strongpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
