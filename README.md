# goit-pythonweb-hw-06

Цей проект демонструє використання SQLAlchemy та Alembic для роботи з базою даних PostgreSQL. Проект включає моделі для студентів, груп, викладачів, предметів та оцінок, а також скрипти для заповнення бази даних випадковими даними та виконання запитів.

## Вимоги

- Python 3.11
- PostgreSQL
- Poetry
- Faker

## Docker (Postgres)

```ini
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```

## Встановлення

1. Клонувати репозиторій:

   ```bash
   git clone https://github.com/yourusername/goit-pythonweb-hw-06.git
   cd goit-pythonweb-hw-06
   ```

2. Встановити залежності за допомогою Poetry:

   ```bash
   poetry install
   ```

3. Налаштувати Alembic:

   ```bash
   alembic init alembic
   ```

4. Налаштувати файл `alembic.ini`:

   ```ini
   sqlalchemy.url = postgresql+psycopg2://postgres:password@localhost/postgres
   ```

5. Створити міграції та застосувати їх:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## Заповнення бази даних

Для заповнення бази даних випадковими даними використовуйте скрипт `seeds.py`:

```bash
poetry run python assessment/seeds.py
```
