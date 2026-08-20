"""Celery-задачи для привычек."""

import logging
from datetime import date

import requests
from django.conf import settings
from django.utils import timezone

from config.celery import app
from habits.models import Habit

logger = logging.getLogger(__name__)


def _send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram Bot API."""
    if not settings.TELEGRAM_BOT_TOKEN:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        with requests.Session() as session:
            session.trust_env = False
            response = session.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.warning("Прямая отправка в Telegram не удалась, пробуем системные proxy-настройки.")

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Не удалось отправить Telegram-напоминание.")
        return False

    return True


@app.task
def send_habit_reminders():
    """Отправляет напоминания о привычках, подходящих по времени и периодичности."""
    now = timezone.localtime()
    today = now.date()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.select_related("user").filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        if not habit.user.telegram_chat_id:
            continue

        if habit.last_notification_date == today:
            continue

        if not _is_habit_due(habit, today):
            continue

        reminder_text = (
            f"Напоминание: в {current_time.strftime('%H:%M')} "
            f"нужно выполнить привычку '{habit.action}' в '{habit.place}'."
        )
        sent = _send_telegram_message(habit.user.telegram_chat_id, reminder_text)
        if sent:
            habit.last_notification_date = today
            habit.save(update_fields=["last_notification_date"])


def _is_habit_due(habit, today: date):
    """Проверяет, нужно ли сегодня напоминать о привычке."""
    if habit.periodicity < 1:
        return False

    start_date = habit.created_at.date()
    days_since_creation = (today - start_date).days
    return days_since_creation % habit.periodicity == 0
