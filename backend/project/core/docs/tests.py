import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from project.accounts.models import User


@pytest.mark.django_db
class TestDocsView:
    """Test API documentation access control."""

    def test_docs_view_requires_authentication(self, api_client: APIClient):
        """Test that unauthenticated users cannot access docs."""
        docs_url = reverse("docs")
        response = api_client.get(docs_url)

        # Should be unauthorized for unauthenticated users (DRF returns 401)
        assert response.status_code == 401

    def test_docs_view_requires_admin(self, api_client: APIClient, user: User):
        """Test that regular authenticated users cannot access docs."""
        # Regular user (not staff)
        api_client.force_authenticate(user=user)
        docs_url = reverse("docs")
        response = api_client.get(docs_url)

        # Should be forbidden for authenticated non-admin users (DRF returns 403)
        assert response.status_code == 403

    def test_docs_view_allows_admin_users(self, api_client: APIClient, site):
        """Test that admin users can access docs."""
        # Create admin user
        admin_user = User.objects.create_user(
            email="admin@example.com",
            site=site,
            name="Admin User",
            password="password123",
            is_staff=True,
        )
        api_client.force_authenticate(user=admin_user)

        docs_url = reverse("docs")
        response = api_client.get(docs_url)

        # Should be accessible for admin users
        assert response.status_code == 200
        # Should contain HTML for Redoc documentation
        assert b"redoc" in response.content.lower()

    def test_schema_endpoint_requires_authentication(self, api_client: APIClient):
        """Test that unauthenticated users cannot access schema."""
        schema_url = reverse("schema")
        response = api_client.get(schema_url)

        # Should be unauthorized for unauthenticated users (DRF returns 401)
        assert response.status_code == 401

    def test_schema_endpoint_requires_admin(self, api_client: APIClient, user: User):
        """Test that regular authenticated users cannot access schema."""
        # Regular user (not staff)
        api_client.force_authenticate(user=user)
        schema_url = reverse("schema")
        response = api_client.get(schema_url)

        # Should be forbidden for authenticated non-admin users (DRF returns 403)
        assert response.status_code == 403

    def test_schema_endpoint_allows_admin_users(self, api_client: APIClient, site):
        """Test that admin users can access schema."""
        # Create admin user
        admin_user = User.objects.create_user(
            email="admin@example.com",
            site=site,
            name="Admin User",
            password="password123",
            is_staff=True,
        )
        api_client.force_authenticate(user=admin_user)

        schema_url = reverse("schema")
        response = api_client.get(schema_url)

        # Should be accessible for admin users
        assert response.status_code == 200
        # Should return OpenAPI schema
        content_type = response.get("Content-Type", "")
        assert any(ct in content_type.lower() for ct in ["json", "yaml", "openapi"])

    def test_superuser_can_access_docs(self, api_client: APIClient, site):
        """Test that superusers can access docs."""
        # Create superuser
        superuser = User.objects.create_superuser(
            email="super@example.com",
            site=site,
            name="Super User",
            password="password123",
        )
        api_client.force_authenticate(user=superuser)

        docs_url = reverse("docs")
        response = api_client.get(docs_url)

        # Should be accessible for superusers
        assert response.status_code == 200
        assert b"redoc" in response.content.lower()

    def test_superuser_can_access_schema(self, api_client: APIClient, site):
        """Test that superusers can access schema."""
        # Create superuser
        superuser = User.objects.create_superuser(
            email="super@example.com",
            site=site,
            name="Super User",
            password="password123",
        )
        api_client.force_authenticate(user=superuser)

        schema_url = reverse("schema")
        response = api_client.get(schema_url)

        # Should be accessible for superusers
        assert response.status_code == 200
        content_type = response.get("Content-Type", "")
        assert any(ct in content_type.lower() for ct in ["json", "yaml", "openapi"])


@pytest.mark.django_db
def test_api_schema_requires_admin(api_client: APIClient):
    """Test that the API schema endpoint requires admin access."""
    response = api_client.get(reverse("schema"))
    # Should be unauthorized for unauthenticated users
    assert response.status_code == 401


@pytest.mark.django_db
def test_docs_work_with_session_auth(client, site):
    """Test that docs work with session authentication (e.g., when logged in via Django admin)."""
    from django.test import Client

    # Create an admin user
    admin_user = User.objects.create_user(
        email="sessionadmin@example.com",
        site=site,
        name="Session Admin",
        password="admin123",
        is_staff=True,
    )

    # Use Django test client (not API client) to simulate session auth
    django_client = Client()

    # Login via session authentication using the INTERNAL username format
    # Django's login() expects the actual username field, not email
    login_success = django_client.login(
        username=admin_user.username,  # Use internal username: "site_id-email"
        password="admin123",
    )
    assert login_success, f"Login should succeed with username: {admin_user.username}"

    # Now try to access the docs with session auth
    docs_response = django_client.get(reverse("docs"))
    assert docs_response.status_code == 200
    assert b"redoc" in docs_response.content.lower()

    # Also test schema endpoint with session auth
    schema_response = django_client.get(reverse("schema"))
    assert schema_response.status_code == 200
    content_type = schema_response.get("Content-Type", "")
    assert any(ct in content_type.lower() for ct in ["json", "yaml", "openapi"])
