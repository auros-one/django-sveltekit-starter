import re
from http import HTTPStatus
from unittest.mock import patch

import pytest
from allauth.account.admin import EmailAddress
from django.core import mail
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from ..models import User


class SiteMiddlewareMixin:
    """Mixin to add site context to requests in tests."""

    def add_site_to_request(self, request, site):
        """Add site to request object like our middleware does."""
        request.site = site


@pytest.mark.django_db
class TestAuth(SiteMiddlewareMixin):
    def test_signup(self, api_client: APIClient, site):
        # sanity checks
        assert User.objects.count() == 0
        assert EmailAddress.objects.count() == 0
        assert len(mail.outbox) == 0

        # Mock the site middleware
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site(request):
                request.site = site
                return None

            mock_middleware.side_effect = add_site

            # create user
            response = api_client.post(
                reverse("custom-signup"),
                {
                    "email": "test@example.com",
                    "password1": "a-super-strong-password-145338-@!#&",
                    "password2": "a-super-strong-password-145338-@!#&",
                },
                HTTP_HOST=site.domain,
            )

        # check results
        assert response.status_code == HTTPStatus.CREATED
        result = response.json()
        assert "access" in result
        assert "refresh" in result
        assert "user" in result
        assert result["user"]["email"] == "test@example.com"

        assert User.objects.count() == 1
        created_user = User.objects.first()
        assert created_user is not None
        assert created_user.site == site
        assert created_user.username == f"{site.pk}-test@example.com"

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
        response = api_client.post(reverse("rest_verify_email"), {"key": key})

        # check results
        assert response.status_code == HTTPStatus.OK
        email_address = EmailAddress.objects.first()
        assert email_address is not None
        assert email_address.verified

    def test_login(self, api_client: APIClient, user: User):
        # Mock site middleware for login
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site(request):
                request.site = user.site
                return None

            mock_middleware.side_effect = add_site

            response = api_client.post(
                reverse("rest_login"),
                {
                    "email": user.email,
                    "password": "a-super-strong-password-145338-@!#&",
                },
                HTTP_HOST=user.site.domain,
            )

        assert response.status_code == HTTPStatus.OK
        assert response.cookies.get("refresh-token") is not None
        result = response.json()
        assert "access" in result
        assert "refresh" in result
        assert "user" in result
        assert result["user"]["email"] == user.email

        # Use the jwt token to make a request to the authcheck view
        response = api_client.get(
            reverse("authcheck"), HTTP_AUTHORIZATION="Bearer " + result["access"]
        )
        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
class TestEmailChangeView(SiteMiddlewareMixin):
    def assert_user_email_didnt_change(self, user: User):
        user.refresh_from_db()

        assert user.email == "test@example.com"

        assert EmailAddress.objects.filter(user=user).count() == 1
        new_email = EmailAddress.objects.filter(user=user).first()
        assert new_email is not None
        assert new_email.email == "test@example.com"
        assert new_email.verified

        assert len(mail.outbox) == 0

        # Test authentication with site-aware method
        authenticated_user = User.objects.authenticate_user(
            "test@example.com", user.site, "a-super-strong-password-145338-@!#&"
        )
        assert authenticated_user == user

    def test_change_email(self, api_client: APIClient, user: User):
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "new_email@example.com",
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.OK  # Returns 200 with message
        assert response.json() == {
            "detail": "Email change initiated. Check your email to confirm."
        }

        user.refresh_from_db()
        assert user.email == "new_email@example.com"
        # Username should also be updated
        assert user.username == f"{user.site.pk}-new_email@example.com"

        assert EmailAddress.objects.filter(user=user).count() == 1
        new_email = EmailAddress.objects.filter(user=user).first()
        assert new_email is not None
        assert new_email.email == "new_email@example.com"
        assert not new_email.verified

        assert len(mail.outbox) == 1  # Email confirmation was sent

        # Test with site-aware authentication
        assert (
            User.objects.authenticate_user(
                "test@example.com", user.site, "a-super-strong-password-145338-@!#&"
            )
            is None
        )

        assert (
            User.objects.authenticate_user(
                "new_email@example.com",
                user.site,
                "a-super-strong-password-145338-@!#&",
            )
            == user
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
        assert response.json() == {"password": ["Invalid password."]}
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
        assert response.json() == {
            "new_email": ["This email address is already in use."]
        }
        self.assert_user_email_didnt_change(user)

    def test_email_already_exists(self, api_client: APIClient, user: User):
        # Create another user in the SAME site to test collision
        other_user = User.objects.create_user(
            email="new_email@example.com",
            site=user.site,  # Same site - should conflict
            name="Another Test User",
            password="another-super-strong-password-145338-@!#&",
        )
        baker.make(EmailAddress, user=other_user, email=other_user.email, verified=True)

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "new_email@example.com",  # This email exists in same site
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "new_email": ["This email address is already in use."]
        }
        self.assert_user_email_didnt_change(user)

    def test_email_exists_in_different_site_allowed(
        self, api_client: APIClient, user: User, site
    ):
        # Create a different site
        from django.contrib.sites.models import Site

        other_site = Site.objects.create(domain="other.example.com", name="Other Site")

        # Create user with same email in different site (should be allowed)
        User.objects.create_user(
            email="shared@example.com",
            site=other_site,  # Different site - should NOT conflict
            name="Other Site User",
            password="another-password",
        )

        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": "shared@example.com",  # This email exists in different site
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        # Should succeed because email is in different site
        assert response.status_code == HTTPStatus.OK  # Returns 200 with message
        assert response.json() == {
            "detail": "Email change initiated. Check your email to confirm."
        }

        user.refresh_from_db()
        assert user.email == "shared@example.com"
        assert user.username == f"{user.site.pk}-shared@example.com"
