import Core.Celery.CeleryBootstrap  # noqa: F401 — register ORM mappers before tasks load

from celery import Celery

from Core.settings import get_celery_broker_url, get_celery_backend_url

celery_app = Celery(
    "Core",
    broker=get_celery_broker_url(),
    backend=get_celery_backend_url(),
    include=["Tasks.test", "Tasks.CancelPendingOrder", "Tasks.SendActivation"],
)

celery_app.conf.beat_schedule = {
    "cancel-pending-orders-every-5-minutes": {
        "task": "Tasks.CancelPendingOrder.cancel_pending_order",
        "schedule": 300.0,
        "kwargs": {"expiration_minutes": 10},
    },
}

celery_app.conf.timezone = "UTC"
