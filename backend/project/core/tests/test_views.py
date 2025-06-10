import pytest
from django.urls import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from project.accounts.models import User


@pytest.mark.django_db
def test_healthcheck(api_client: APIClient) -> None:
    response = api_client.get(reverse("healthcheck"))
    assert response.status_code == 204


@pytest.mark.django_db
def test_authcheck(api_client: APIClient, user: User):
    # Test view without authentication
    response = api_client.get(reverse("authcheck"))
    assert response.status_code == HTTP_401_UNAUTHORIZED

    # Test view with authentication
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("authcheck"))
    assert response.status_code == HTTP_204_NO_CONTENT
