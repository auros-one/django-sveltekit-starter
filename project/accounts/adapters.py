from allauth.account.adapter import DefaultAccountAdapter

from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        """

        if settings.ENVIRONMENT == "development":
            base_url = (
                f"http://{settings.FRONTEND_DOMAIN}{settings.EMAIL_VERIFICATION_PATH}"
            )
        else:  # pragma: no cover
            base_url = (
                f"https://{settings.FRONTEND_DOMAIN}{settings.EMAIL_VERIFICATION_PATH}"
            )

        url = f"{base_url}?key={emailconfirmation.key}"

        return url
