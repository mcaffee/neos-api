from core.injector import configure_injector
from core.celery import app as celery_app

__all__ = ('celery_app',)


configure_injector()
