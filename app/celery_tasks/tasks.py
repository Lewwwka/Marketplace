import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.database import get_sync_db
from app.db.models import Order
from app.core.config import settings
from app.celery_tasks.celery import celery_app


@celery_app.task
def process_order(order_id: int):
    db = next(get_sync_db())
    result = db.execute(
        select(Order)
        .options(selectinload(Order.items), selectinload(Order.user))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if order:
        send_order_email.delay(order_id, order.user.email)


@celery_app.task
def send_order_email(order_id: int, user_email: str):
    db = next(get_sync_db())
    try:
        result = db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = user_email
        msg["Subject"] = f"Новый заказ #{order_id}"

        html = f"""
            <h2>Спасибо за заказ #{order_id}</h2>
            <p>Сумма: {order.total_price}₽</p>
            <ul>
            """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email отправлен для заказа {order.id}")

    except Exception as e:
        print(f"Ошибка отправки email {order_id}: {e}")
