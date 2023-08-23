import pytest
from hypothesis import given
from hypothesis.extra.django import from_field
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from django import forms
from project.accounts.models import User

from .fields import SlugField


@given(slug=from_field(SlugField(blank=True)))
def test_slugfield_form(slug):
    class SlugFieldForm(forms.Form):
        slug = SlugField(blank=True).formfield()

    form = SlugFieldForm(data={"slug": slug})
    assert form.is_valid()


def test_healthcheck(api_client: APIClient) -> None:
    response = api_client.get("/healthcheck/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_api_key_permission(api_client: APIClient, user: User):
    # Test view without API key
    response = api_client.get("/authcheck/")
    assert response.status_code == HTTP_401_UNAUTHORIZED

    # Test view with API key
    api_client.force_authenticate(user=user)
    response = api_client.get("/authcheck/")
    assert response.status_code == HTTP_204_NO_CONTENT
