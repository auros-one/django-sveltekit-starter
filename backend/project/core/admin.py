from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularRedocView

from project.core.docs.utils import get_docs_title
from project.core.utils.frontend import get_frontend_base_url

# We try to get the site name from the database, but this won't work
# on a fresh project that hasn't done any migrations yet.
try:
    from django.contrib.sites.models import Site

    site_name = Site.objects.get_current().name
except Exception:  # pragma: no cover
    site_name = "Project Backend"


class CustomAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = f"{site_name} admin"

    # Text to put in each page's <h1> (and above login form).
    site_header = f"{site_name} administration"

    # Text to put at the top of the admin index page.
    index_title = f"{site_name} administration"

    # The URL for the “View site” link at the top of each admin page.
    site_url = get_frontend_base_url()

    def get_urls(self):

        urls = super().get_urls()
        urls = [
            path(
                "docs/",
                self.admin_view(
                    SpectacularRedocView.as_view(
                        url_name="schema", title=get_docs_title()
                    )
                ),
                name="docs",
            )
        ] + urls
        return urls
