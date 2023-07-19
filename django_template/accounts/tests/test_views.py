from http import HTTPStatus

import pytest
from django.core import mail
from rest_framework.test import APIClient

from ..models import User


@pytest.mark.django_db
class TestAuth:
    def test_signup(self, api_client: APIClient):
        assert User.objects.count() == 0
        assert len(mail.outbox) == 0

        response = api_client.post(
            "/accounts/signup/",
            {
                "email": "test@example.com",
                "password1": "a-super-strong-password-145338-@!#&",
                "password2": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert User.objects.count() == 1
        assert len(mail.outbox) == 1

    def test_login(self, api_client: APIClient):
        user = User.objects.create_user(
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
        assert response.data["key"] == user.auth_token.key
