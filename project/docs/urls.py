from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from django.conf import settings
from django.urls import path

docs_title = settings.SPECTACULAR_SETTINGS["TITLE"]
try:
    # We try to get the site name from the database, but this won't work
    # on a fresh project that hasn't done any migrations yet.
    from django.contrib.sites.models import Site

    site_name = Site.objects.get_current().name
    docs_title += f" | {site_name} admin"
except Exception:  # pragma: no cover
    pass


urlpatterns = [
    path(
        "",
        SpectacularRedocView.as_view(url_name="schema", title=docs_title),
        name="docs",
    ),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
]
