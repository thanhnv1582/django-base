"""
Pytest configuration and shared fixtures.

All fixtures here are available to ALL tests without imports.
"""
import pytest
from django.test import Client
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def django_db_setup():
    """Use the test database defined in test.py settings (SQLite in-memory)."""


@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(db, django_user_model) -> APIClient:
    """API client authenticated as a test user."""
    user = django_user_model.objects.create_user(
        email="test@example.com",
        password="testpass123!",
        full_name="Test User",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def test_user(db, django_user_model):
    """A basic test user instance."""
    return django_user_model.objects.create_user(
        email="user@example.com",
        password="testpass123!",
        full_name="Regular User",
    )


@pytest.fixture
def admin_user(db, django_user_model):
    """A staff/admin test user."""
    return django_user_model.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123!",
        full_name="Admin User",
    )
