from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from dj_rest_auth.serializers import (
    PasswordResetSerializer as RestAuthPasswordResetSerializer,
)
from django.conf import settings
from rest_framework import serializers

from .models import User


class RegisterSerializer(BaseRegisterSerializer):
    """
    Site-aware registration serializer that creates users with proper site context.
    """

    name = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_email(self, email):
        """Validate that email doesn't already exist in this site."""
        site = self.context.get("site")

        if email and site:
            if User.objects.filter(email__iexact=email, site=site).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists in this site."
                )

        return email

    def get_cleaned_data(self):
        """Override to include site in cleaned data."""
        data = super().get_cleaned_data()
        data["name"] = self.validated_data.get("name", "")

        # Get site from context (added by our CustomRegisterView)
        site = self.context.get("site")
        if site:
            data["site"] = site

        return data

    def save(self, request):
        """Override to create user with site context."""
        site = self.context.get("site")
        if not site:
            raise serializers.ValidationError(
                "Site context is required for registration"
            )

        email = self.validated_data.get("email")
        password = self.validated_data.get("password1")
        name = self.validated_data.get("name", "")

        # Create user with site context
        user = User.objects.create_user(
            email=email, site=site, name=name, password=password
        )

        return user


class LoginSerializer(RestAuthLoginSerializer):
    """
    Site-aware login serializer that allows email-based login while using
    site-scoped username internally.

    Users still login with email + password, but authentication happens with
    the internal username format: "site_id-email"
    """

    username = None  # Remove username field from parent
    email = serializers.EmailField(required=True)

    def authenticate(self, **credentials):
        """
        Override to handle site-aware authentication.
        Convert email to internal username format for Django auth.
        """
        email = credentials.get("email")
        password = credentials.get("password")

        if email and password:
            # Get site from request context
            request = self.context.get("request")
            if not request or not hasattr(request, "site"):
                raise serializers.ValidationError(
                    "Site context is required for authentication"
                )

            site = request.site

            # Use our custom authentication method
            return User.objects.authenticate_user(email, site, password)

        return None


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User serializer that only exposes public fields.
    Username is internal and never exposed to frontend.
    """

    class Meta:
        model = User
        fields = ("email", "name", "is_superuser")  # Only public fields
        read_only_fields = ("email", "is_superuser")


class EmailChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user email address.
    Updates both the public email and internal username.
    """

    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context["request"].user
        password = attrs["password"]
        new_email = attrs["new_email"]

        # Verify password
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid password."})

        # Check if email already exists in this site
        if User.objects.filter(email__iexact=new_email, site=user.site).exists():
            raise serializers.ValidationError(
                {"new_email": "This email address is already in use."}
            )

        return attrs


class PasswordResetSerializer(RestAuthPasswordResetSerializer):
    """
    Site-aware password reset serializer.
    """

    def get_email_options(self):
        """Override to include site context in password reset emails."""
        request = self.context.get("request")
        opts = {
            "use_https": request.is_secure() if request else False,
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
        }

        if hasattr(request, "site") and request is not None:
            opts["domain_override"] = request.site.domain

        return opts
