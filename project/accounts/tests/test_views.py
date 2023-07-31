import re
from http import HTTPStatus

import pytest
from allauth.account.admin import EmailAddress
from django.core import mail
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
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == "test@example.com"

        assert User.objects.count() == 1
        assert EmailAddress.objects.count() == 1
        assert not EmailAddress.objects.first().verified
        assert len(mail.outbox) == 1

        # get the verify key from the verification url
        url_match = re.search(r'http[^"\']+?/(?=\s)', mail.outbox[0].body)  # type: ignore
        assert url_match is not None, "No URL found in the email body"
        verification_url = url_match.group()  # type: ignore
        key = [item for item in verification_url.split("/") if item][-1]  # type: ignore

        # verify email
        response = api_client.post("/accounts/signup/verify-email/", {"key": key})

        # check results
        assert response.status_code == HTTPStatus.OK
        assert EmailAddress.objects.first().verified

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
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == "test@example.com"
