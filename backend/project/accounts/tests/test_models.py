import pytest
from django.db import IntegrityError, transaction

from ..models import User


@pytest.mark.django_db
class TestUser:
    def test_create_user(self):
        user = User.objects.create_user(
            email="piet@example.com",
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        assert user.email == "piet@example.com"
        assert user.name == "Piet Mondrian"
        assert not user.is_staff
        assert not user.is_superuser
        # Password should be hashed.
        assert user.password != "correcthorsebatterystaple"

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="piet@example.com",
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        assert user.email == "piet@example.com"
        assert user.name == "Piet Mondrian"
        assert user.is_staff
        assert user.is_superuser
        # Password should be hashed.
        assert user.password != "correcthorsebatterystaple"

    def test_get_user_by_case_insensitive_email(self):
        user = User.objects.create_user(
            email="fRoMThENiNEtiEs@example.com",
            name="l33t h4x0r",
            password="trustno1",
        )
        assert User.objects.get_by_natural_key("fromthenineties@example.com") == user

    def test_email_case_insensitively_unique(self):
        User.objects.create_user(
            email="piet@example.com",
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        with pytest.raises(
            IntegrityError, match="duplicate key value violates unique constraint"
        ), transaction.atomic():
            User.objects.create_user(
                email="Piet@example.com",
                name="Piet Mondrian",
                password="correcthorsebatterystaple",
            )
        # Using exactly the same email should also fail.
        with pytest.raises(
            IntegrityError, match="duplicate key value violates unique constraint"
        ), transaction.atomic():
            User.objects.create_user(
                email="piet@example.com",
                name="Piet Mondrian",
                password="correcthorsebatterystaple",
            )

    def test_str(self):
        user = User.objects.create_user(
            email="piet@example.com",
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        assert str(user) == "piet@example.com"
