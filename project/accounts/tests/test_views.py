import re
from http import HTTPStatus

import pytest
from allauth.account.admin import EmailAddress
from django.contrib.auth import authenticate
from django.core import mail
from django.urls import reverse
from model_bakery import baker
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
        key_match = re.search(r"key=([a-zA-Z0-9-_:]+)", mail.outbox[0].body)
        assert key_match is not None
        key = key_match.group(1)

        # verify email
        response = api_client.post("/accounts/signup/verify-email/", {"key": key})

        # check results
        assert response.status_code == HTTPStatus.OK
        email_address = EmailAddress.objects.first()
        assert email_address is not None
        assert email_address.verified

    def test_login(self, api_client: APIClient, user: User):
        response = api_client.post(
            "/accounts/login/",
            {
                "email": user.email,
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.OK
        assert response.cookies.get("refresh-token") is not None
        result = response.json()
        assert "access" in result
        assert "refresh" in result
        assert "user" in result
        assert result["user"]["email"] == user.email

        # Use the jwt token to make a request to the /authcheck/ view
        response = api_client.get(
            "/authcheck/", HTTP_AUTHORIZATION="Bearer " + result["access"]
        )
        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
class TestEmailChangeView:
    def assert_user_email_didnt_change(self, user: User):
        user.refresh_from_db()

        assert user.email == "test@example.com"

        assert EmailAddress.objects.filter(user=user).count() == 1
        new_email = EmailAddress.objects.filter(user=user).first()
        assert new_email is not None
        assert new_email.email == "test@example.com"
        assert new_email.verified

        assert len(mail.outbox) == 0

        assert authenticate(
            username="test@example.com", password="a-super-strong-password-145338-@!#&"
        )

    def test_change_email(self, api_client: APIClient, user: User):
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

        assert EmailAddress.objects.filter(user=user).count() == 1
        new_email = EmailAddress.objects.filter(user=user).first()
        assert new_email is not None
        assert new_email.email == "new_email@example.com"
        assert not new_email.verified

        assert len(mail.outbox) == 1  # Email confirmation was sent

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

    def test_invalid_password(self, api_client: APIClient, user: User):
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "new_email@example.com",
                "password": "wrong-password",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "Incorrect password."}
        self.assert_user_email_didnt_change(user)

    def test_identical_email(self, api_client: APIClient, user: User):
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "test@example.com",
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "This email is already in use."}
        self.assert_user_email_didnt_change(user)

    def test_email_already_exists(self, api_client: APIClient, user: User):
        other_user = User.objects.create_user(
            "new_email@example.com",
            name="Another Test User",
            password="another-super-strong-password-145338-@!#&",
        )
        baker.make(EmailAddress, user=other_user, email=other_user.email, verified=True)

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "test@example.com",
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "This email is already in use."}
        self.assert_user_email_didnt_change(user)
