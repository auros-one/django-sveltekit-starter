import pytest
import yaml
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse

from project.accounts.models import User


@pytest.mark.django_db
class TestDocsView:

    def test_docs_view_is_protected(self, client: Client):
        docs_url = reverse("admin:docs")
        response = client.get(docs_url)
        assert response.status_code == 302
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == f"/api/admin/login/?next={docs_url}"

    def test_docs_view_requires_admin(self, client: Client, user: User):
        client.force_login(user)
        docs_url = reverse("admin:docs")
        response = client.get(docs_url)
        assert response.status_code == 302
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == f"/api/admin/login/?next={docs_url}"

    def test_docs_view_renders(self, client: Client):
        # Login as superuser
        superuser = User.objects.create_superuser(
            email="admin@admin.com",
            name="Admin",
            password="password1!65è4ç6!",
        )
        client.force_login(superuser)

        response = client.get(reverse("admin:docs"))

        assert response.status_code == 200
        data = response.data  # type: ignore[attr-defined]
        assert data["title"] == "API Documentation | example.com admin"
        assert data["schema_url"] == reverse("schema")


def test_api_schema(client: Client):
    response = client.get(reverse("schema"))
    assert response.status_code == 200
    assert len(response.content) > 0

    # use pyyaml to parse the OpenAPI schema
    schema = yaml.safe_load(response.content)
    assert isinstance(schema, dict)
    assert "openapi" in schema
    assert "paths" in schema
    assert schema["info"]["title"] == "API Documentation"
