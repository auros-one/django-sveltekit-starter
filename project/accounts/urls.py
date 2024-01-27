from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from rest_framework.authtoken.models import TokenProxy

from django.contrib import admin
from django.urls import include, path
from project.accounts.views import ChangeEmailView

urlpatterns = [
    path("signup/", include("dj_rest_auth.registration.urls"), name="signup"),
    path("", include("dj_rest_auth.urls")),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
]


# We can't unregister these in the admin.py file because they won't be registered yet.
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(TokenProxy)
