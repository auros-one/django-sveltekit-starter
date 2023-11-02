import re
from http import HTTPStatus

import pytest
from allauth.account.admin import EmailAddress
from django.contrib.auth import authenticate
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import User


@pytest.mark.django_db
class TestAuth:
    def test_signup(self, api_client: APIClient):
        # sanity checks
        assert User.objects.count() == 0
        assert EmailAddress.objects.count() == 0
        assert len(mail.outbox) == 0

        # create user
        response = api_client.post(
            "/accounts/signup/",
            {
                "email": "test@example.com",
                "password1": "a-super-strong-password-145338-@!#&",
                "password2": "a-super-strong-password-145338-@!#&",
            },
        )

        # check results
        assert response.status_code == HTTPStatus.CREATED
        result = response.json()
        assert "access" in result
        assert "refresh" in result
        assert "user" in result
        assert result["user"]["email"] == "test@example.com"

        assert User.objects.count() == 1
        assert EmailAddress.objects.count() == 1
        email_address = EmailAddress.objects.first()
        assert email_address is not None
        assert not email_address.verified
        assert len(mail.outbox) == 1

        # get the verify key from the verification url
        key_match = re.search(r"key=([a-zA-Z0-9-_:]+)", mail.outbox[0].body)  # type: ignore
        key = key_match.group(1)  # type: ignore

        # verify email
        response = api_client.post("/accounts/signup/verify-email/", {"key": key})

        # check results
        assert response.status_code == HTTPStatus.OK
        email_address = EmailAddress.objects.first()
        assert email_address is not None
        assert email_address.verified

    def test_login(self, api_client: APIClient):
        User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="a-super-strong-password-145338-@!#&",
        )

        response = api_client.post(
            "/accounts/login/",
            {
                "email": "test@example.com",
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.OK
        assert response.cookies.get("refresh-token") is not None
        result = response.json()
        assert "access" in result
        assert "refresh" in result
        assert "user" in result
        assert result["user"]["email"] == "test@example.com"


@pytest.mark.django_db
class TestEmailChangeView:
    def test_change_email(self, api_client: APIClient):
        user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="a-super-strong-password-145338-@!#&",
        )

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "new_email@example.com",
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        user.refresh_from_db()
        assert user.email == "new_email@example.com"

        assert (
            authenticate(
                username="test@example.com",
                password="a-super-strong-password-145338-@!#&",
            )
            is None
        )
        assert authenticate(
            username="new_email@example.com",
            password="a-super-strong-password-145338-@!#&",
        )

    def test_invalid_password(self, api_client: APIClient):
        user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="a-super-strong-password-145338-@!#&",
        )

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "new_email@example.com",
                "password": "wrong-password",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        user.refresh_from_db()
        assert user.email == "test@example.com"

        assert authenticate(
            username="test@example.com", password="a-super-strong-password-145338-@!#&"
        )
        assert (
            authenticate(
                username="new_email@example.com",
                password="a-super-strong-password-145338-@!#&",
            )
            is None
        )

    def test_identical_email(self, api_client: APIClient):
        user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="a-super-strong-password-145338-@!#&",
        )

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "test@example.com",
                "password": "wrong-password",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        user.refresh_from_db()
        assert user.email == "test@example.com"

        assert authenticate(
            username="test@example.com", password="a-super-strong-password-145338-@!#&"
        )
