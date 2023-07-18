from django.apps import AppConfig
from django.db.models import CharField
from django.db.models.functions import Length


class UtilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_template.utils"

    def ready(self) -> None:
        CharField.register_lookup(Length)
