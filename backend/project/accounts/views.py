from allauth.account.models import EmailAddress
from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import EmailChangeSerializer, RegisterSerializer


class CustomRegisterView(RegisterView):
    """
    Site-aware registration view.
    Adds site context to the serializer and handles site-specific signup.
    """

    serializer_class = RegisterSerializer

    def get_serializer_context(self):
        """Add site context from request."""
        context = super().get_serializer_context()

        # Get site from request (added by SiteMiddleware)
        request = self.request
        if hasattr(request, "site"):
            context["site"] = request.site

        return context


class ChangeEmailView(generics.GenericAPIView):
    serializer_class = EmailChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_email = serializer.validated_data["new_email"]

        # Check if email already exists in current site (excluding current user)
        if (
            User.objects.filter(email__iexact=new_email, site=user.site)
            .exclude(pk=user.pk)
            .exists()
        ):
            return Response(
                {"new_email": ["This email address is already in use."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update email and username (which includes the email)
        user.email = new_email
        user.username = f"{user.site.pk}-{new_email}"
        user.save()

        # Update or create EmailAddress for allauth
        with transaction.atomic():
            EmailAddress.objects.filter(user=user).delete()
            email_address = EmailAddress.objects.create(
                user=user,
                email=new_email,
                primary=True,
                verified=False,  # Require re-verification
            )

        # Send confirmation email
        email_address.send_confirmation(request=request)

        return Response(
            {"detail": "Email change initiated. Check your email to confirm."},
            status=status.HTTP_200_OK,
        )
