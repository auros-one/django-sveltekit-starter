from django.apps import AppConfig
from django.db.models import CharField
from django.db.models.functions import Length


class DocsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project.docs"

    def ready(self):
        CharField.register_lookup(Length)
