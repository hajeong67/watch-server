import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'send_reserved_msgs': {
    #     'task': 'notifications.tasks.send_reserved_msgs',
    #     'schedule': crontab(minute='*/10'),
    # },
    'save_login_log': {
        'task': 'companies.tasks.save_login_log',
        'schedule': crontab(minute=0, hour=0),
        # 'schedule': crontab(minute='*/1'),
    },
    # 'store_positioning_engine_cache': {
    #     'task': 'positioning.tasks.restore_all_positioning_engine_cache',
    #     'schedule': crontab(minute='*/10'),
    # }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')