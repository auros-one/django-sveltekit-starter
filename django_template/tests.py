from django.test import Client


def test_homepage_renders(client: Client):
    """Test that the homepage exists."""
    response = client.get("/")
    assert response.status_code == 200
