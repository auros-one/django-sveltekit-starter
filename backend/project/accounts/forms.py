from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.forms import AllAuthPasswordResetForm


class CustomPasswordResetForm(AllAuthPasswordResetForm):
    """
    Custom password reset form that generates frontend URLs instead of Django URLs.
    """

    def save(self, request=None, **kwargs):
        """
        Generate a password reset email with a frontend URL.
        """
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:
            # Generate the password reset key
            uid = user_pk_to_url_str(user)
            token = token_generator.make_token(user)
            key = f"{uid}-{token}"

            # Get the adapter and use its method to generate the frontend URL
            from allauth.account.adapter import get_adapter

            adapter = get_adapter(request)
            url = adapter.get_reset_password_from_key_url(key)

            # Send the email
            context = {
                "user": user,
                "password_reset_url": url,
                "request": request,
            }

            # Use allauth's email sending
            from allauth.account.adapter import get_adapter

            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )

        return self.cleaned_data["email"]
