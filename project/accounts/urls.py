from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialToken
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.authtoken.models import TokenProxy

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
