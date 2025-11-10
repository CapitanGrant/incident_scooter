# UCar Top Doer

Микросервис для управления задачами (тестовое задание).

## Описание

FastAPI-сервис для учёта инцидентов.

Позволяет принимать от операторов и систем сообщения о проблемах в TG (самокат не в сети, точка не отвечает, отчёт не
выгрузился).
и регистрирует данные сообщения в удобном формате, в данном случае в бд.

## Технологический стек

- **Python 3.12**
- **FastAPI 0.104.1** - современный веб-фреймворк
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL** - основная база данных
- **Alembic** - миграции базы данных
- **Pydantic 2.5** - валидация данных
- **Docker** - контейнеризация
- **Poetry** - управление зависимостями

## Требования

- Python 3.12+
- PostgreSQL
- Poetry

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/CapitanGrant/incident_scooter
cd incident_scooter
```

2. Для быстрого запуска с помощью Docker:

```bash
# Запуск всех сервисов
docker-compose up -d --build

# Остановка
docker-compose down
```

3. Для ручной установки, установите зависимости через Poetry:

```bash
poetry install
```

4. Настройте переменные окружения (создайте файл .env):

```bash
# Основная база данных
DB_USER=postgres_user
DB_PASSWORD=postgres_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=postgres_db

# Тестовая база данных  
TEST_DB_HOST=localhost
TEST_DB_PORT=5444
TEST_DB_NAME=postgres_db
TEST_DB_URL="postgresql+asyncpg://postgres_user:postgres_password@localhost:5444/postgres_db"
```

5. Запустите миграции:

```bash
alembic upgrade head
```

6. Запустите приложение:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

7. Документация будет доступна по url:

```bash
http://localhost:8000/docs

```
