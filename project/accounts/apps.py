from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project.accounts"

    def ready(self):
        # import KnoxTokenScheme so it's loaded for drf-spectacular
        # https://github.com/tfranzel/drf-spectacular/issues/264#issuecomment-1317781295
        from project.schema import JWTSchema  # noqa: F401  # type: ignore
