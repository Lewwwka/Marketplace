# API Магазина - FastAPI + PostgreSQL + Redis + Celery

REST API для интернет-магазина с авторизацией, товарами, заказами, корзиной и уведомлениями на почту

# Используемый стек технологий

| Категория      | Технология              | Версия  | Описание                          |
| -------------- | ----------------------- | ------- | --------------------------------- |
| Framework      | FastAPI                 | 0.129.0 | Современный быстрый веб-фреймворк |
| База данных    | PostgreSQL              | 17.0    | Реляционная БД                    |
| ORM            | SQLAlchemy              | 2.0.46  | Async ORM для PostgreSQL          |
| ASGI сервер    | Uvicorn                 | 0.41.0  | ASGI сервер                       |
| Модели         | Pydantic V2             | 2.13.0  | Валидация данных                  |
| Миграции       | Alembic                 | 1.18.4  | Миграции БД                       |
| Docker         | Docker Compose          | 29.1.3  | Контейнеризация                   |
| Аутентификация | JWT                     | -       | Bearer токены                     |
| Кэш            | Redis                   | 7.2.0   | Корзина товаров                   |
| Очереди задач	 | Celery                  | 5.6.2   | Асинхронная обработка             |
| Брокер сообщений|RabbitMQ	               | 0.2.0   | Очередь для Celery                |
| Уведомления	Email| SMTP	                 | -	     | Отправка писем при заказе         |
| Тестирование   | pytest + pytest-asyncio | 9.0.2   | Тесты                             |

[![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-brightgreen)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.0-blue)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-orange)](https://www.sqlalchemy.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.41.0-yellow)](https://www.uvicorn.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-blueviolet)](https://docs.pydantic.dev/latest/)
[![Alembic](https://img.shields.io/badge/Alembic-1.18.4-teal)](https://alembic.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)
[![JWT](https://img.shields.io/badge/JWT-Bearer%20Tokens-000000)](https://jwt.io/)
[![Redis](https://img.shields.io/badge/Redis-7.2.0-red)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6.2-green)](https://docs.celeryq.dev/en/stable/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-0.2.0-pink)](https://www.rabbitmq.com/)
[![SMTP](https://img.shields.io/badge/Email-SMTP-yellowgreen)](https://www.ietf.org/rfc/rfc5321.txt)
[![Pytest](https://img.shields.io/badge/pytest-9.0.2-purple)](https://docs.pytest.org/)

# Запуск приложения через Docker Compose
Убедись, что установлены:
* Docker
* Docker Compose

```bash
git clone <repo-url>
cd marketplace
cp .env.example .env

```
* Отредактируй пароли в .env:
- SECRET_KEY="JWT KEY"
- EMAIL_FROM="Email с которого будут приходить сообщения"
- EMAIL_PASSWORD="Пароль приложений"
* Для отправки уведомлений необходимо создать пароль приложений gmail: https://myaccount.google.com/apppasswords

Запуск проекта
```bash
docker-compose up --build
```
# API Docs: 
http://localhost:8000/docs 

<img width="1011" height="805" alt="{80F3EDC7-967A-4A33-AEA0-454BB582DEEC}" src="https://github.com/user-attachments/assets/2058e2b8-9bcc-43d8-959e-041d70115033" />

# Запуск тестов
```bash
docker compose exec app uv run pytest -v
```
<img width="894" height="435" alt="{24A2F0A1-D398-42BA-9F61-A19B2150EB36}" src="https://github.com/user-attachments/assets/9bad2a3a-9665-49ed-aa09-bcc3a5d91ddf" />

# Пример уведомления на почту при заказе
<img width="579" height="275" alt="{623F5299-F158-4F55-B229-3150C8424631}" src="https://github.com/user-attachments/assets/cd29d393-5b7d-40d1-94e1-149de7aad4f7" />

