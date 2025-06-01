from django.conf import settings


def get_docs_title() -> str:
    docs_title = settings.SPECTACULAR_SETTINGS["TITLE"]
    try:
        # We try to get the site name from the database, but this won't work
        # on a fresh project that hasn't done any migrations yet.
        from django.contrib.sites.models import Site

        site_name = Site.objects.get_current().name
        docs_title += f" | {site_name} admin"
    except Exception:  # pragma: no cover
        pass
    return docs_title
