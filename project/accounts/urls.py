from django.urls import include
from django.urls import path

from project.accounts.views import ChangeEmailView

urlpatterns = [
    path("signup/", include("dj_rest_auth.registration.urls"), name="signup"),
    path("", include("dj_rest_auth.urls")),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
]
