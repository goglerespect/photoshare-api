# PhotoShare API

Backend API для сервісу обміну фотографіями, побудований на FastAPI відповідно до ТЗ: https://docs.google.com/document/d/1iiZ7yycTjvdqkXCjKn4W-BzWs3mP1Uuls8fgQL-Biwk/edit?tab=t.0

## Основні можливості

- JWT авторизація
- Ролі користувачів (user / moderator / admin)
- Завантаження фотографій
- Інтеграція з Cloudinary
- Генерація QR-кодів
- Коментарі до фотографій
- Система рейтингів
- Пошук та фільтрація користувачів
- Docker підтримка
- PostgreSQL база даних
- Автоматичне тестування через Pytest
- Покриття тестами понад 90%

---

## Технології

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Cloudinary
- Pytest

---

## Live Demo
https://yummy-starlene-goit12-88bd75cd.koyeb.app/docs

Локальний запуск проекту:

Клонування репозиторію:
git clone https://github.com/goglerespect/photoshare-api

Створення .env:
CLOUDINARY_CLOUD_NAME="dcmgcnk7k"
CLOUDINARY_API_KEY="219446151441865"
CLOUDINARY_API_SECRET="cZJR3hz4PjvZt4csmqvrsd3HDRQ"

DATABASE_URL=postgresql://neondb_owner:npg_5wpCsb7FJNGi@ep-frosty-hall-alby9xaf.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=mysecret123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Запуск через Docker:
docker compose up --build

Запуск тестів:
pytest --cov=app

Поточне покриття тестами:
92%

Структура проекту
app/
├── core/
├── models/
├── routes/
├── schemas/
tests/

Деплой:
Проект задеплоєний за допомогою:
Koyeb
Neon PostgreSQL

Автор:
Бекенд-проект, створений для навчальних цілей та портфоліо.