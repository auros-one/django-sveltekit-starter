from django.conf import settings
from django.contrib import admin

# We try to get the site name from the database, but this won't work
# on a fresh project that hasn't done any migrations yet.
try:
    from django.contrib.sites.models import Site

    site_name = Site.objects.get_current().name
except Exception:
    site_name = "Project Backend"


class CustomAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = f"{site_name} admin"

    # Text to put in each page's <h1> (and above login form).
    site_header = f"{site_name} administration"

    # Text to put at the top of the admin index page.
    index_title = f"{site_name} administration"

    # The URL for the “View site” link at the top of each admin page.
    if settings.ENVIRONMENT == "development":
        site_url = f"http://{settings.FRONTEND_DOMAIN}/"
    else:
        site_url = f"https://{settings.FRONTEND_DOMAIN}/"
