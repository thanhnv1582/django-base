"""Make config a Python package. Also exposes the Celery app for workers."""
from .celery import app as celery_app

__all__ = ["celery_app"]
