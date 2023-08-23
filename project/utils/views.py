from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import PublicReadOnly


class HealthCheck(APIView):
    """
    Healthcheck endpoint.
    """

    permission_classes = [PublicReadOnly]

    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthCheck(APIView):
    """
    A private Healthcheck endpoint used for testing API key permissions.
    """

    def get(self, _):
        return Response(status=status.HTTP_204_NO_CONTENT)
