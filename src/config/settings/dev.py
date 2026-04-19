"""Development settings — extends base.py."""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]  # noqa: S104

# Dev-only apps
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

# Dev-only middleware (Debug Toolbar must be early)
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ["127.0.0.1"]

# Simple email backend (print to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Show all SQL queries in tests/dev
LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"  # noqa: F405
