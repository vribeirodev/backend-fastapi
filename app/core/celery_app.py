import os
from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest@rabbitmq//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "db+postgresql://admin:masterkey@db/db_project")
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
)

celery_app.autodiscover_tasks(['app.worker.tasks'])
