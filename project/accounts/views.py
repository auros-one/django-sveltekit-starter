from allauth.account.admin import EmailAddress
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from project.accounts.serializers import EmailChangeSerializer


class ChangeEmailView(APIView):
    serializer_class = EmailChangeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data["new_email"]
        password = serializer.validated_data["password"]

        current_email: EmailAddress | None = EmailAddress.objects.filter(
            user=request.user
        ).first()

        if not current_email:  # pragma: no cover
            # This should never occur: a user should always have an email
            raise APIException("No email found for this user.")

        # Verify if the provided password is correct
        user = request.user
        authenticated_user = authenticate(username=user.email, password=password)
        if not authenticated_user:
            return Response(
                {"detail": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check that nobody else has this email
        if EmailAddress.objects.filter(email=new_email).exists():
            return Response(
                {"detail": "This email is already in use."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the email
        with transaction.atomic():
            current_email.delete()
            new_email_record = EmailAddress.objects.create(user=user, email=new_email)
            new_email_record.send_confirmation(request=request, signup=False)
            user.email = new_email
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
