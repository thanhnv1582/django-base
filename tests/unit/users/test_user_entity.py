"""
Unit tests for UserEntity — no DB, no Django, pure Python.

Tests: entity creation, domain events, business rules.
"""
import pytest

from apps.users.domain.entities.user import UserEntity
from apps.users.domain.events.user_registered import UserRegistered
from apps.users.domain.events.user_deactivated import UserDeactivated
from apps.users.domain.value_objects.email import Email
from core.exceptions.base import BusinessRuleException, ValidationException


@pytest.mark.unit
class TestUserEntity:
    """Tests for UserEntity business rules — no DB required."""

    def test_register_creates_user_with_correct_data(self):
        user = UserEntity.register(email="alice@example.com", full_name="Alice Smith")

        assert user.email.value == "alice@example.com"
        assert user.full_name.value == "Alice Smith"
        assert user.is_active is True
        assert user.is_admin is False

    def test_register_raises_user_registered_event(self):
        user = UserEntity.register(email="bob@example.com", full_name="Bob Jones")
        events = user.pull_events()

        assert len(events) == 1
        assert isinstance(events[0], UserRegistered)
        assert events[0].email == "bob@example.com"

    def test_pull_events_clears_event_list(self):
        user = UserEntity.register(email="c@example.com", full_name="Charlie")
        user.pull_events()

        assert user.pull_events() == []

    def test_deactivate_sets_is_active_false(self):
        user = UserEntity.register(email="d@example.com", full_name="Dana")
        user.deactivate()

        assert user.is_active is False

    def test_deactivate_raises_event(self):
        user = UserEntity.register(email="e@example.com", full_name="Eve")
        user.pull_events()  # clear registration event
        user.deactivate()

        events = user.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], UserDeactivated)

    def test_cannot_deactivate_already_inactive_user(self):
        user = UserEntity.register(email="f@example.com", full_name="Frank")
        user.deactivate()

        with pytest.raises(BusinessRuleException, match="already deactivated"):
            user.deactivate()

    def test_entity_equality_by_id(self):
        user1 = UserEntity.register(email="g@example.com", full_name="Grace")
        user2 = UserEntity.register(email="h@example.com", full_name="Hank")

        assert user1 != user2
        assert user1 == user1


@pytest.mark.unit
class TestEmailValueObject:
    """Tests for Email Value Object validation."""

    def test_valid_email_normalizes_to_lowercase(self):
        email = Email(value="ALICE@EXAMPLE.COM")
        assert email.value == "alice@example.com"

    def test_invalid_email_raises_validation_exception(self):
        with pytest.raises(ValidationException, match="not a valid email"):
            Email(value="not-an-email")

    def test_email_strips_whitespace(self):
        email = Email(value="  bob@test.com  ")
        assert email.value == "bob@test.com"

    def test_email_frozen_immutable(self):
        email = Email(value="test@example.com")
        with pytest.raises(Exception):
            email.value = "changed@example.com"  # type: ignore[misc]
