from celery import shared_task
from app.db.database import get_db
from app.db.models import Order


@shared_task
def process_order(order_id: int):
    db = next(get_db())
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            send_order_email.delay(order_id)
    finally:
        db.close()


@shared_task
def send_order_email(order_id: int):
    pass
