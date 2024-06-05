from allauth.account.admin import EmailAddress
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import (
    PasswordResetSerializer as RestAuthPasswordResetSerializer,
)
from django.conf import settings
from rest_framework import serializers

from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField()

    def get_verified(self, obj) -> bool:
        user_emails = EmailAddress.objects.filter(user=obj)
        if user_emails:
            return user_emails[0].verified
        else:
            return False

    class Meta:
        model = User
        fields = ("email", "verified")


class PasswordResetSerializer(RestAuthPasswordResetSerializer):
    """
    Overwrite dj-rest-auths PasswordResetSerializer to accept a custom password reset link.

    It does so by adding the a custom url_generator to the AllAuthPasswordResetForm.save()
    options.
    """

    def save(self):
        if "allauth" in settings.INSTALLED_APPS:
            from allauth.account.forms import default_token_generator
        else:
            from django.contrib.auth.tokens import default_token_generator

        # Overwrite the url_generator with a custom one.
        if settings.ENVIRONMENT == "development":
            base_url = f"http://{settings.FRONTEND_DOMAINS[0]}{settings.PASSWORD_CONFIRM_RESET_PATH}"
        else:
            base_url = f"https://{settings.FRONTEND_DOMAINS[0]}{settings.PASSWORD_CONFIRM_RESET_PATH}"

        def _url_generator(request, user, temp_key):
            return f"{base_url}?uid={user_pk_to_url_str(user)}&token={temp_key}"

        request = self.context.get("request")
        # Set some values to trigger the send_email method.
        opts = {
            "use_https": request.is_secure(),  # type: ignore[attr-defined]
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
            "token_generator": default_token_generator,
            "url_generator": _url_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)  # type: ignore[attr-defined]


class EmailChangeSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    password = serializers.CharField()
