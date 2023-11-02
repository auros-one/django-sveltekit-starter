from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from project.accounts.serializers import EmailChangeSerializer


class ChangeEmailView(APIView):
    serializer_class = EmailChangeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data["new_email"]
        password = serializer.validated_data["password"]

        # Verify if the provided password is correct
        user = request.user
        authenticated_user = authenticate(username=user.email, password=password)
        if not authenticated_user:
            return Response(
                {"detail": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check that it's not the same emails
        if request.user.email == new_email:
            return Response(
                {"detail": "The provided email is the same as the current one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the email
        user.email = new_email
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
