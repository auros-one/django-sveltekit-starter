from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.authtoken.models import TokenProxy

from project.accounts.views import ChangeEmailView, CustomRegisterView

urlpatterns = [
    # Custom signup view (overrides the default)
    path("signup/", CustomRegisterView.as_view(), name="custom-signup"),
    # Email verification URLs from dj_rest_auth.registration
    re_path(r"verify-email/?$", VerifyEmailView.as_view(), name="rest_verify_email"),
    re_path(
        r"resend-email/?$",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    re_path(
        r"account-email-verification-sent/?$",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    # Include all other dj_rest_auth URLs
    path("", include("dj_rest_auth.urls")),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
]


# We can't unregister these in the admin.py file because they won't be registered yet.
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(TokenProxy)
