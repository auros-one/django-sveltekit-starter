import pytest
import respx
from allauth.account.admin import EmailAddress
from django.contrib.sites.models import Site
from django.test.utils import override_settings
from hypothesis.extra.django._fields import _for_slug, register_for
from model_bakery import baker
from model_bakery.random_gen import gen_slug, gen_text
from rest_framework.test import APIClient

from project.accounts.models import User
from project.core import fields


def _gen_slug(max_length: int = 500) -> str:  # pragma: no cover
    """Generate a slug."""
    # model-bakery requires a max_length, but our SlugField doesn't.
    # The only change here is to add a default to the max_length parameter.
    return gen_slug(max_length)


baker.generators.add("project.core.fields.SlugField", _gen_slug)
baker.generators.add("project.core.fields.StringField", gen_text)


@register_for(fields.SlugField)
def for_slug(field):
    # We need to use some internal API here because there's no other way
    # to get generic text that works properly (other than copy/paste I suppose).
    return _for_slug(field)


TEST_SETTINGS = {
    "CACHES": {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    "PASSWORD_HASHERS": ["django.contrib.auth.hashers.MD5PasswordHasher"],
    "STORAGES": {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    },
    "WHITENOISE_AUTOREFRESH": True,
}


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    """Override settings for tests."""
    with override_settings(**TEST_SETTINGS):
        yield


@pytest.fixture(scope="session", autouse=True)
def ensure_http_requests_handled():
    """Ensure all httpx requests are handled.
    Any test that uses httpx will fail if all requests aren't mocked out with respx.
    """
    with respx.mock:
        yield


@pytest.fixture
def api_client() -> APIClient:
    """Return a DRF API client instance."""
    return APIClient()


@pytest.fixture
def site():
    """Test site fixture."""
    return Site.objects.create(domain="testsite.localhost", name="Test Site")


@pytest.fixture
def other_site():
    """Another test site fixture for multi-tenant testing."""
    return Site.objects.create(domain="othersite.localhost", name="Other Site")


@pytest.fixture
def user(site):
    """Test user fixture with site context."""
    user = User.objects.create_user(
        email="test@example.com",
        site=site,
        name="Test User",
        password="a-super-strong-password-145338-@!#&",
    )
    baker.make(EmailAddress, user=user, email=user.email, verified=True, primary=True)
    return user


@pytest.fixture
def other_user(other_site):
    """Test user in different site for multi-tenant testing."""
    other_user = User.objects.create_user(
        email="other-test-user@example.com",
        site=other_site,
        name="Other User",
        password="other-super-strong-password-145338-@!#&",
    )
    baker.make(
        EmailAddress,
        user=other_user,
        email=other_user.email,
        verified=True,
        primary=True,
    )
    return other_user


@pytest.fixture
def same_site_user(site):
    """Another user in the same site as the main user fixture."""
    same_site_user = User.objects.create_user(
        email="samesite@example.com",
        site=site,
        name="Same Site User",
        password="same-site-password-123",
    )
    baker.make(
        EmailAddress,
        user=same_site_user,
        email=same_site_user.email,
        verified=True,
        primary=True,
    )
    return same_site_user
