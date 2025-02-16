from celery.loaders import app
from celery.schedules import crontab

app.conf.beat_schedule = {
    'execute-orders-every-minute': {
        'task': 'trading.tasks.execute_orders',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}