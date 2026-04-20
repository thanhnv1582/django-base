"""Users app configuration."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    label = "users"
    verbose_name = "Users"

    def ready(self) -> None:
        """Import signals when the app is ready."""
        # import apps.users.infrastructure.signals  # Uncomment when signals added
