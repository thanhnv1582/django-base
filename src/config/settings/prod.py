"""Production settings — extends base.py. Security hardened."""
from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

# ─── HTTPS & Security Headers ─────────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ─── Email (SMTP) ─────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")  # noqa: F405
EMAIL_PORT = env.int("EMAIL_PORT", default=587)  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # noqa: F405
DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER", default="noreply@example.com")  # noqa: F405

# ─── Production Logging ───────────────────────────────────────────────────────
LOGGING["handlers"]["file"] = {  # noqa: F405
    "level": "WARNING",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": "/var/log/django/app.log",
    "maxBytes": 1024 * 1024 * 10,  # 10 MB
    "backupCount": 5,
    "formatter": "json",
}
LOGGING["root"]["handlers"] = ["console", "file"]  # noqa: F405
