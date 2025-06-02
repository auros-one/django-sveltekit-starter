from django.conf import settings


def get_frontend_base_url():
    if settings.ENVIRONMENT == "development":
        return f"http://{settings.FRONTEND_DOMAINS[0]}"
    else:
        return f"https://{settings.FRONTEND_DOMAINS[0]}"
