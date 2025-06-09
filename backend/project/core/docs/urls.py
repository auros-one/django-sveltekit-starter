from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authentication import SessionAuthentication

from project.core.docs.utils import get_docs_title
from project.core.permissions import IsAdminUser


class AdminOnlySpectacularRedocView(SpectacularRedocView):
    """
    Redoc view that requires admin permissions.
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTCookieAuthentication, SessionAuthentication]


class AdminOnlySpectacularAPIView(SpectacularAPIView):
    """
    Schema API view that requires admin permissions.
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTCookieAuthentication, SessionAuthentication]


urlpatterns = [
    path(
        "",
        AdminOnlySpectacularRedocView.as_view(
            url_name="schema", title=get_docs_title()
        ),
        name="docs",
    ),
    path("schema/", AdminOnlySpectacularAPIView.as_view(), name="schema"),
]
