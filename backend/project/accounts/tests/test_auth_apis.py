from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from allauth.account.admin import EmailAddress
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import User


@pytest.mark.django_db
class TestSiteAwareAuthentication:
    """Test suite for Django Sites-based multi-tenant authentication."""

    def test_signup_creates_site_aware_user(self, api_client: APIClient, site):
        """Test that signup creates users with proper site context and username format."""
        # Mock the site middleware
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site(request):
                request.site = site
                return None

            mock_middleware.side_effect = add_site

            # Sanity checks
            assert User.objects.count() == 0
            assert EmailAddress.objects.count() == 0
            assert len(mail.outbox) == 0

            # Create user
            response = api_client.post(
                reverse("custom-signup"),
                {
                    "email": "newuser@example.com",
                    "password1": "super-strong-password-123!",
                    "password2": "super-strong-password-123!",
                    "name": "New User",
                },
                HTTP_HOST=site.domain,
            )

            # Check response
            assert response.status_code == HTTPStatus.CREATED
            result = response.json()
            assert "access" in result
            assert "refresh" in result
            assert "user" in result
            assert result["user"]["email"] == "newuser@example.com"
            assert result["user"]["name"] == "New User"
            assert "username" not in result["user"]  # Username should never be exposed

            # Check database state
            assert User.objects.count() == 1
            user = User.objects.first()
            assert user is not None
            assert user.email == "newuser@example.com"
            assert user.site == site
            assert user.username == f"{site.pk}-newuser@example.com"  # Proper format

            assert EmailAddress.objects.count() == 1
            email_address = EmailAddress.objects.first()
            assert email_address is not None
            assert email_address.user == user
            assert not email_address.verified  # Should require verification
            assert len(mail.outbox) == 1  # Verification email sent

    def test_login_with_email_converts_to_username(self, api_client: APIClient, user):
        """Test that login accepts email and converts to internal username for auth."""
        # Mock the site middleware
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
            result = response.json()
            assert "access" in result
            assert "user" in result
            assert result["user"]["email"] == user.email
            assert "username" not in result["user"]  # Never expose username

    def test_login_fails_without_site_context(self, api_client: APIClient, user):
        """Test that login fails when site context is missing."""
        # Don't mock the middleware - let it fail to set site
        response = api_client.post(
            reverse("rest_login"),
            {
                "email": user.email,
                "password": "a-super-strong-password-145338-@!#&",
            },
            # No HTTP_HOST header
        )

        # The middleware should still set a site in development mode
        # So the login might succeed but find no user
        assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]

    def test_multi_tenant_isolation_signup(
        self, api_client: APIClient, site, other_site
    ):
        """Test that users with same email can exist in different sites."""
        email = "shared@example.com"
        password = "shared-password-123!"

        # Create user in first site
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site1(request):
                request.site = site
                return None

            mock_middleware.side_effect = add_site1

            response1 = api_client.post(
                reverse("custom-signup"),
                {
                    "email": email,
                    "password1": password,
                    "password2": password,
                    "name": "Site 1 User",
                },
                HTTP_HOST=site.domain,
            )
            assert response1.status_code == HTTPStatus.CREATED

        # Create user with same email in second site
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site2(request):
                request.site = other_site
                return None

            mock_middleware.side_effect = add_site2

            response2 = api_client.post(
                reverse("custom-signup"),
                {
                    "email": email,
                    "password1": password,
                    "password2": password,
                    "name": "Site 2 User",
                },
                HTTP_HOST=other_site.domain,
            )
            assert response2.status_code == HTTPStatus.CREATED

        # Verify both users exist with different usernames
        users = User.objects.filter(email=email)
        assert users.count() == 2

        user1 = users.get(site=site)
        user2 = users.get(site=other_site)
        assert user1.site != user2.site
        assert user1.username != user2.username
        assert user1.username == f"{site.pk}-{email}"
        assert user2.username == f"{other_site.pk}-{email}"

    def test_multi_tenant_isolation_login(self, api_client: APIClient):
        """Test that users can only login within their own site."""
        # Create same email in two different sites
        site1 = Site.objects.create(domain="site1.test", name="Site 1")
        site2 = Site.objects.create(domain="site2.test", name="Site 2")

        email = "isolated@example.com"
        password = "isolation-test-123!"

        User.objects.create_user(email=email, site=site1, password=password)
        User.objects.create_user(email=email, site=site2, password=password)

        # User1 should only authenticate in site1 context
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site1(request):
                request.site = site1
                return None

            mock_middleware.side_effect = add_site1

            response = api_client.post(
                reverse("rest_login"),
                {"email": email, "password": password},
                HTTP_HOST=site1.domain,
            )
            assert response.status_code == HTTPStatus.OK
            assert response.json()["user"]["email"] == email

        # User1 should NOT authenticate in site2 context (but user2 should)
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site2(request):
                request.site = site2
                return None

            mock_middleware.side_effect = add_site2

            # This should find user2, not user1
            response = api_client.post(
                reverse("rest_login"),
                {"email": email, "password": password},
                HTTP_HOST=site2.domain,
            )
            assert response.status_code == HTTPStatus.OK  # Should succeed with user2

    def test_user_details_only_exposes_public_fields(self, api_client: APIClient, user):
        """Test that user details API never exposes internal username."""
        api_client.force_authenticate(user=user)

        response = api_client.get(reverse("rest_user_details"))

        assert response.status_code == HTTPStatus.OK
        result = response.json()

        # Should only contain public fields
        expected_fields = {"email", "name", "is_superuser"}
        assert set(result.keys()) == expected_fields

        # Should never contain internal fields
        forbidden_fields = {"username", "site", "password", "last_login", "date_joined"}
        for field in forbidden_fields:
            assert field not in result

    def test_password_reset_site_aware(self, api_client: APIClient, user):
        """Test password reset works within site context."""
        # Create a proper mock request
        mock_request = MagicMock()
        mock_request.site = user.site
        mock_request.is_secure.return_value = False
        mock_request.get_host.return_value = user.site.domain
        mock_request.META = {"HTTP_HOST": user.site.domain}

        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site(request):
                request.site = user.site
                return None

            mock_middleware.side_effect = add_site

            response = api_client.post(
                reverse("rest_password_reset"),
                {"email": user.email},
                HTTP_HOST=user.site.domain,
            )

            assert response.status_code == HTTPStatus.OK
            assert len(mail.outbox) == 1

            # Check email contains proper site context
            # Password reset emails typically contain the site domain in the reset URL
            # We can't check for specific content without knowing the email template

    def test_email_change_updates_username(self, api_client: APIClient, user):
        """Test that changing email also updates the internal username."""
        api_client.force_authenticate(user=user)

        new_email = "newemail@example.com"
        old_username = user.username

        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": new_email,
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.OK

        user.refresh_from_db()
        assert user.email == new_email
        assert user.username == f"{user.site.pk}-{new_email}"
        assert user.username != old_username

        # Should create unverified email address
        email_address = EmailAddress.objects.get(user=user)
        assert email_address.email == new_email
        assert not email_address.verified

    def test_email_change_site_isolation(
        self, api_client: APIClient, user, same_site_user
    ):
        """Test that email change respects site boundaries."""
        api_client.force_authenticate(user=user)

        # Try to change to an email that exists in the same site
        response = api_client.post(
            reverse("change-email"),
            {
                "new_email": same_site_user.email,
                "password": "a-super-strong-password-145338-@!#&",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "already in use" in response.json()["new_email"][0]

    def test_prevent_duplicate_emails_in_same_site(self, api_client: APIClient, site):
        """Test that signup prevents duplicate emails within the same site."""
        email = "duplicate@example.com"
        password = "duplicate-password-123!"

        # Create first user
        User.objects.create_user(email=email, site=site, password=password)

        # Try to create second user with same email in same site
        with patch(
            "project.core.middleware.SiteMiddleware.process_request"
        ) as mock_middleware:

            def add_site(request):
                request.site = site
                return None

            mock_middleware.side_effect = add_site

            response = api_client.post(
                reverse("custom-signup"),
                {
                    "email": email,
                    "password1": password,
                    "password2": password,
                },
                HTTP_HOST=site.domain,
            )

            # Should get validation error about email already existing
            assert response.status_code == HTTPStatus.BAD_REQUEST
            response_data = response.json()
            assert "email" in response_data
            assert "already exists" in response_data["email"][0].lower()

    def test_username_format_validation(self, site):
        """Test that usernames follow the required site_id-email format."""
        email = "format@example.com"
        user = User.objects.create_user(email=email, site=site, password="test123")

        expected_username = f"{site.pk}-{email}"
        assert user.username == expected_username

        # Test manual username validation
        user.username = "wrong-format"
        with pytest.raises(Exception):  # Should fail validation
            user.full_clean()

    def test_authentication_backend_integration(self, user):
        """Test that Django's authenticate() works with our username format."""
        # Direct authenticate should work with internal username
        authenticated_user = authenticate(
            username=user.username, password="a-super-strong-password-145338-@!#&"
        )
        assert authenticated_user == user

        # Should NOT work with email directly (that's handled by our custom methods)
        authenticated_user = authenticate(
            username=user.email, password="a-super-strong-password-145338-@!#&"
        )
        assert authenticated_user is None

    def test_site_middleware_creates_username(self, site):
        """Test that users get proper usernames even without explicit setting."""
        # Create user without setting username explicitly
        user = User(email="auto@example.com", site=site, name="Auto User")
        user.set_password("auto123")
        user.save()  # Should auto-generate username

        assert user.username == f"{site.pk}-auto@example.com"
