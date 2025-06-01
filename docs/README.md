# GeoApp

GeoApp е уеб приложение за обозначаване на прерятствия по пътя с REST API и визуализация на карта. Проектът използва FastAPI, SQLAlchemy и Docker.

Функционалности

- Добавяне на точка с координати и описание
- Преглед на всички точки в списък и на карта
- Редактиране и изтриване на точки
- HTML визуален интерфейс
- REST API (достъпен през `/docs`)

Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL (или SQLite за тестове)
- Jinja2 (шаблони)
- Leaflet.js (карта)
- Docker
- pytest (тестове)

Стартиране с Docker

1. Създай `.env` файл в `backend/`:

DB_USER=
DB_PASSWORD=
DB_NAME=
DB_HOST=
DB_PORT=

2. Стартирай проекта:

docker-compose up --build

3. Отвори браузъра на: `http://localhost:8000/map`

Тестване

cd backend

(използва SQLite като in-memory база за тестове)
