from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from drf_spectacular.utils import OpenApiResponse  # type: ignore
from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from revproxy.views import ProxyView

from .permissions import PublicReadOnly


class HealthCheck(APIView):
    """
    Healthcheck endpoint.
    """

    permission_classes = [PublicReadOnly]

    @extend_schema(
        operation_id="Health Check",
        responses={204: None},
        tags=["Checks"],
    )
    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthCheck(APIView):
    """
    A private Healthcheck endpoint used for testing API key permissions.
    """

    @extend_schema(
        operation_id="Auth Check",
        responses={
            "204": OpenApiResponse(description="Authenticated."),
            "403": OpenApiResponse(description="Not authenticated."),
        },
        tags=["Checks"],
    )
    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlowerProxyView(LoginRequiredMixin, UserPassesTestMixin, ProxyView):
    upstream = (
        f"http://{settings.DOKKU_APP_NAME}.flower.1:5555/api/admin/flower/"
        if settings.ENVIRONMENT == "production"
        else "http://celery_flower:5555/api/admin/flower/"
    )  # type: ignore

    def test_func(self):
        return self.request.user.is_superuser  # type: ignore
