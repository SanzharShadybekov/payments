import os
from celery import Celery
from celery.schedules import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-payment-status-every-minute': {
        'task': 'core.tasks.check_payment_status',
        'schedule': schedule(run_every=10),  # Каждые 10 сек
    },
}
