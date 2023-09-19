import yaml

from django.test import Client
from django.urls import reverse


def test_docs_view_renders(client: Client):
    response = client.get(reverse("docs"))
    assert response.status_code == 200
    assert len(response.content) > 0


def test_api_schema(client: Client):
    response = client.get(reverse("schema"))
    assert response.status_code == 200
    assert len(response.content) > 0

    # use pyyaml to parse the OpenAPI schema
    schema = yaml.safe_load(response.content)
    assert isinstance(schema, dict)
    assert "openapi" in schema
    assert "paths" in schema
    assert schema["info"]["title"] == "Project API"
