from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from project.core.utils.frontend import get_frontend_base_url


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        """
        base_url = get_frontend_base_url()
        url = (
            f"{base_url}{settings.EMAIL_VERIFICATION_PATH}?key={emailconfirmation.key}"
        )
        return url

    def get_reset_password_from_key_url(self, key):
        """
        Constructs the password reset confirmation URL that points to the frontend.
        This is called when generating the password reset email.
        """
        base_url = get_frontend_base_url()
        # The key contains both uid and token, but we need them separate for the frontend
        # The key format from allauth is "uid-token"
        # We'll pass the full key and let the frontend parse it
        url = f"{base_url}{settings.PASSWORD_CONFIRM_RESET_PATH}?key={key}"
        return url
