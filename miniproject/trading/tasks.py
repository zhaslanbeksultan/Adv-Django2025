from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def execute_orders():
    pending_orders = Order.objects.filter(status='PENDING')
    for order in pending_orders:
        try:
            order.execute()
        except ValueError:
            pass

@shared_task
def send_trade_notification(user_email, message):
    send_mail(
        'Trade Executed',
        message,
        'zhaslanbeksultan@gmail.com',
        [user_email],
        fail_silently=False,
    )