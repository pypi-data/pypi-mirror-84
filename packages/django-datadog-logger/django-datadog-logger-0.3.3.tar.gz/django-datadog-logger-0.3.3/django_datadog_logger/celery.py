from functools import wraps
from uuid import uuid4

from celery import Task
from celery.utils.threads import release_local

from django_datadog_logger.local import Local  # NOQA

local = Local()


def get_celery_request():
    try:
        return local.request
    except AttributeError:
        return None


def store_celery_request(func):
    @wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            if args and isinstance(args[0], Task) and hasattr(args[0], "request"):
                local.request = args[0].request
            return func(*args, **kwargs)
        finally:
            release_local(local)

    return function_wrapper


__all__ = ["local", "get_celery_request", "store_celery_request"]
