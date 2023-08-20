import pytest
import respx
from hypothesis.extra.django._fields import _for_slug, register_for
from model_bakery import baker
from model_bakery.random_gen import gen_slug, gen_text
from rest_framework.test import APIClient

from django.test.utils import override_settings
from project.utils import fields


def _gen_slug(max_length: int = 500) -> str:  # pragma: no cover
    """Generate a slug."""
    # model-bakery requires a max_length, but our SlugField doesn't.
    # The only change here is to add a default to the max_length parameter.
    return gen_slug(max_length)


baker.generators.add("project.utils.fields.SlugField", _gen_slug)
baker.generators.add("project.utils.fields.StringField", gen_text)


@register_for(fields.SlugField)
def for_slug(field):
    # We need to use some internal API here because there's no other way
    # to get generic text that works properly (other than copy/paste I suppose).
    return _for_slug(field)


TEST_SETTINGS = {
    "CACHES": {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    "PASSWORD_HASHERS": ["django.contrib.auth.hashers.MD5PasswordHasher"],
    "STATICFILES_STORAGE": "django.contrib.staticfiles.storage.StaticFilesStorage",
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
