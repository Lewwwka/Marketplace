from celery import shared_task
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import Order


@shared_task
async def process_order(order_id: int):
    async with get_db() as db:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if order:
            send_order_email.delay(order_id)


@shared_task
def send_order_email(order_id: int):
    print(f"Отправка сообщения на почту с заказом {order_id}")
