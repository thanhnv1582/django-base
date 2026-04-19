"""
Integration tests for Users API — tests the full HTTP stack.
"""
import pytest
from django.urls import reverse


@pytest.mark.integration
@pytest.mark.django_db
class TestRegisterUserAPI:
    """Tests for POST /api/v1/auth/register/"""

    def test_register_success_returns_201(self, api_client):
        payload = {
            "email": "newuser@example.com",
            "password": "Str0ngPass!",
            "full_name": "New User",
        }
        response = api_client.post("/api/v1/auth/register/", payload)

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "newuser@example.com"
        assert "id" in data["data"]

    def test_register_duplicate_email_returns_409(self, api_client, test_user):
        payload = {
            "email": test_user.email,
            "password": "Str0ngPass!",
            "full_name": "Duplicate User",
        }
        response = api_client.post("/api/v1/auth/register/", payload)

        assert response.status_code == 409
        error = response.json()["error"]
        assert error["code"] == "EMAIL_ALREADY_REGISTERED"

    def test_register_invalid_email_returns_400(self, api_client):
        payload = {
            "email": "not-valid-email",
            "password": "Str0ngPass!",
            "full_name": "Test User",
        }
        response = api_client.post("/api/v1/auth/register/", payload)

        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_register_short_password_returns_400(self, api_client):
        payload = {
            "email": "short@example.com",
            "password": "123",
            "full_name": "Short Pass",
        }
        response = api_client.post("/api/v1/auth/register/", payload)

        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.django_db
class TestUserProfileAPI:
    """Tests for GET /api/v1/users/me/"""

    def test_get_profile_authenticated_returns_200(self, authenticated_client):
        response = authenticated_client.get("/api/v1/users/me/")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"

    def test_get_profile_unauthenticated_returns_401(self, api_client):
        response = api_client.get("/api/v1/users/me/")

        assert response.status_code == 401
        assert response.json()["error"]["code"] == "AUTHENTICATION_FAILED"
