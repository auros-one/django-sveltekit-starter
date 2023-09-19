from drf_spectacular.utils import OpenApiResponse, extend_schema  # type: ignore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import PublicReadOnly


@extend_schema(
    operation_id="Health Check",
    responses={
        "204": OpenApiResponse(description="Authenticated."),
        "403": OpenApiResponse(description="Not authenticated."),
    },
    tags=["Checks"],
)
class HealthCheck(APIView):
    """
    Healthcheck endpoint.
    """

    permission_classes = [PublicReadOnly]

    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    operation_id="Auth Check",
    responses={
        "204": OpenApiResponse(description="Service is running."),
    },
    tags=["Checks"],
)
class AuthCheck(APIView):
    """
    A private Healthcheck endpoint used for testing API key permissions.
    """

    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)
