"""Test settings — fast, isolated, no external dependencies."""
from .base import *  # noqa: F401, F403

DEBUG = False

# ─── Use SQLite in-memory for speed ──────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# ─── Faster password hashing in tests ────────────────────────────────────────
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# ─── Disable Redis — use local memory cache ───────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# ─── Disable Celery — run tasks synchronously ────────────────────────────────
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ─── Disable Sentry in tests ──────────────────────────────────────────────────
SENTRY_DSN = ""

# ─── Email backend ────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ─── Disable throttling in tests ─────────────────────────────────────────────
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []  # noqa: F405
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}  # noqa: F405

# ─── Silence migrations for speed ────────────────────────────────────────────
# Uncomment if you want to skip migrations in tests (faster but less accurate)
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#     def __getitem__(self, item):
#         return None
# MIGRATION_MODULES = DisableMigrations()
