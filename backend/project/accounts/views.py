from allauth.account.admin import EmailAddress
from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from project.accounts.models import User
from project.accounts.serializers import EmailChangeSerializer, RegisterSerializer


class CustomRegisterView(RegisterView):
    """
    Site-aware user registration view.
    """

    serializer_class = RegisterSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add site to context for the serializer
        if hasattr(self.request, "site"):
            context["site"] = self.request.site
        return context

    def create(self, request, *args, **kwargs):
        # Ensure site context is available
        if not hasattr(request, "site") or not request.site:
            return Response(
                {"detail": "Site context is required for registration."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class ChangeEmailView(APIView):
    """
    Site-aware email change view.
    Updates both public email and internal username.
    """

    serializer_class = EmailChangeSerializer

    def post(self, request):
        serializer = EmailChangeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data["new_email"]

            # Check if email already exists in current site
            if User.objects.filter(email__iexact=new_email, site=user.site).exists():
                return Response(
                    {"new_email": ["This email address is already in use."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                # Get current email record
                current_email = EmailAddress.objects.get(user=user, primary=True)
            except EmailAddress.DoesNotExist:
                return Response(
                    {"detail": "No primary email found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the email and username
            with transaction.atomic():
                current_email.delete()
                new_email_record = EmailAddress.objects.create(
                    user=user, email=new_email
                )
                new_email_record.send_confirmation(request=request, signup=False)
                user.email = new_email
                # Update internal username to match new email (site_id-email format)
                user.username = f"{user.site.pk}-{new_email}"
                user.save()

            return Response(
                {"detail": "Email change initiated. Check your email to confirm."}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
