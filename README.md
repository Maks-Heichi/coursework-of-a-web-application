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
- Docker Compose (Django, PostgreSQL, Redis, Celery, Nginx)
- CI/CD через GitHub Actions

## Запуск через Docker Compose (рекомендуется)

Нужен [Docker Desktop](https://www.docker.com/products/docker-desktop/) или Docker + Compose на Linux.

1. Скопируй шаблон окружения:
   ```bash
   copy .env.template .env
   ```
2. Заполни `.env`:
   - `SECRET_KEY` (обязательно)
   - `POSTGRES_*` и `DB_*` (пароль одинаковый)
   - для Docker: `DB_HOST=db`, `CELERY_BROKER_URL=redis://redis:6379/0`
   - Telegram: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
   - в `ALLOWED_HOSTS` добавь IP сервера при деплое
3. Запуск одной командой:
   ```bash
   docker compose up --build
   ```
   Фоном:
   ```bash
   docker compose up -d --build
   ```

Сервисы:
- **nginx** — вход (`http://localhost`), reverse-proxy
- **web** — Django + Gunicorn (`expose 8000`)
- **db** — PostgreSQL (`expose 5432`)
- **redis** — брокер Celery (`expose 6379`)
- **celery** / **celery_beat** — фоновые задачи

У сервисов `restart: unless-stopped`.

Остановка:
```bash
docker compose down
```

Ссылки после запуска:
- API / Swagger: `http://localhost/swagger/`
- Admin: `http://localhost/admin/`

## CI/CD (GitHub Actions)

Файл: `.github/workflows/ci.yml`

Порядок: **test → lint → build → deploy**

- `push` / `pull_request` — test, lint, build
- `deploy` — только при push в `coursework-docker-ci` или `develop`

### Secrets (Settings → Secrets and variables → Actions)

| Secret | Пример |
|--------|--------|
| `SSH_KEY` | приватный ключ (`id_rsa`) |
| `SSH_USER` | `student` или `coursework` |
| `SERVER_IP` | публичный IP ВМ |
| `DEPLOY_DIR` | `/home/student/coursework-of-a-web-application` |

### Сервер

1. Ubuntu + Docker + Compose:
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose-v2
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   ```
   Перелогиниться, проверить `docker ps`.
2. Клон:
   ```bash
   git clone https://github.com/Maks-Heichi/coursework-of-a-web-application.git
   cd coursework-of-a-web-application
   git checkout coursework-docker-ci
   cp .env.template .env
   nano .env
   ```
3. `docker compose up -d --build`
4. Группа безопасности: **TCP 22**, **TCP 80** (8000 наружу не открывать).

После успешного Actions сайт: `http://IP_СЕРВЕРА/swagger/`

## Запуск без Docker (локально)

```bash
poetry install
copy .env.template .env
```

В `.env` для локального запуска без Docker:
- `DB_HOST=127.0.0.1`
- `CELERY_BROKER_URL=redis://localhost:6379/0`
- `CELERY_RESULT_BACKEND=redis://localhost:6379/0`

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Redis отдельно, затем:

```bash
poetry run celery -A config worker -l info -P eventlet
poetry run celery -A config beat -l info
```

## Telegram

Создай бота через `@BotFather`, добавь токен и `chat_id` в `.env`.

## Эндпоинты

Без авторизации:
- `POST /users/register/`
- `POST /token/`
- `POST /token/refresh/`

С авторизацией:
- `GET/POST /habits/`, CRUD привычек
- `GET /habits/public/`

## Тесты

```bash
poetry run python manage.py test
```

## Файлы Docker / CI

- `Dockerfile` — образ Django/Celery/Gunicorn
- `nginx/` — Nginx reverse-proxy
- `docker-compose.yml` — все сервисы
- `.github/workflows/ci.yml` — pipeline
- `.env.template` — шаблон окружения (`.env` в git не попадает)
