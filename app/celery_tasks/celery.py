from celery import Celery
from app.core.config import settings

celery_app = Celery("marketplace")

celery_app.conf.update(
    broker_url=settings.RABBITMQ_URL,
    result_backend=settings.REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    enable_utc=True,
    include=["app.celery_tasks.tasks"],
)

celery_app.autodiscover_tasks()
