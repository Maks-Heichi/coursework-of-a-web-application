# Курсовая работа. Трекер привычек

Проект на Django и DRF.

Что сделано:
- регистрация и авторизация по email
- CRUD привычек
- список публичных привычек
- пагинация
- валидаторы
- Celery + Redis
- напоминания в Telegram

## База данных

Используется PostgreSQL.

Нужно создать базу `coursework_web_app` и заполнить `.env`.

Шаблон:

```bash
copy .env.template .env
```

Потом применить миграции:

```bash
poetry run python manage.py migrate
```

## Запуск проекта

Через Poetry:

```bash
poetry install
copy .env.template .env
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Через requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Redis и Celery

Отдельно нужно запустить Redis.

Потом в одном терминале:

```bash
poetry run celery -A config worker -l info -P eventlet
```

Во втором:

```bash
poetry run celery -A config beat -l info
```

## Telegram

Нужно создать бота через `@BotFather`, получить токен и `chat_id`, потом добавить их в `.env`.

## Ссылки

- API: `http://127.0.0.1:8000/`
- Swagger: `http://127.0.0.1:8000/swagger/`
- Redoc: `http://127.0.0.1:8000/redoc/`
- Admin: `http://127.0.0.1:8000/admin/`

## Эндпоинты

Без авторизации:
- `POST /users/register/`
- `POST /token/`
- `POST /token/refresh/`

С авторизацией:
- `GET /users/`
- `GET /users/{id}/`
- `PUT/PATCH /users/{id}/update/`
- `DELETE /users/{id}/delete/`
- `GET /habits/`
- `POST /habits/create/`
- `GET /habits/{id}/`
- `PUT/PATCH /habits/{id}/update/`
- `DELETE /habits/{id}/delete/`
- `GET /habits/public/`

## Пример создания привычки

```json
{
  "place": "Дом",
  "time": "20:22:00",
  "action": "Выпить стакан воды",
  "is_pleasant": false,
  "related_habit": null,
  "periodicity": 1,
  "reward": "Похвалить себя",
  "execution_time": 60,
  "is_public": true
}
```

## Валидаторы

- нельзя указывать и `reward`, и `related_habit` одновременно
- время выполнения не больше 120 секунд
- периодичность должна быть от 1 до 7 дней
- в связанную привычку можно передавать только приятную
- приятная привычка не может иметь награду или связанную привычку

## Тесты

```bash
poetry run python manage.py test
poetry run coverage run manage.py test
poetry run coverage report
```

Покрытие сейчас около `90%`.

## Файлы проекта

- **manage.py** — команды Django
- **pyproject.toml** — зависимости Poetry
- **requirements.txt** — зависимости для `pip install -r requirements.txt`
- **.env.template** — шаблон переменных окружения
- **.env** — локальные секреты и настройки
- **.flake8** — настройки flake8
**config/settings.py** — настройки проекта, PostgreSQL, DRF, JWT, Celery  
**config/urls.py** — главные маршруты  
**config/celery.py** — конфигурация Celery  
**config/wsgi.py** — запуск на сервере  
**config/asgi.py** — асинхронный запуск  
**users/models.py** — кастомный пользователь  
**users/managers.py** — менеджер пользователей  
**users/serializers.py** — сериализаторы регистрации и профиля  
**users/views.py** — API пользователей и JWT  
**users/urls.py** — маршруты пользователей  
**habits/models.py** — модель привычки  
**habits/serializers.py** — сериализаторы привычек  
**habits/views.py** — CRUD и публичный список привычек  
**habits/tasks.py** — Celery-задача напоминаний  
**habits/paginators.py** — пагинация по 5 элементов  
**habits/permissions.py** — доступ только владельцу  
**tests/test_users_api.py** — тесты пользователей  
**tests/test_habits_api.py** — тесты привычек
