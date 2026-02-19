from celery import Celery
from app.core.config import settings

app = Celery("marketplace")

app.conf.update(
    broker_url=settings.RABBITMQ_URL,
    result_backend=settings.REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    enable_utc=True,
)


if __name__ == "__main__":
    app.start()
