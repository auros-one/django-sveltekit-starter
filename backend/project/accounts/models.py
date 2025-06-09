from __future__ import annotations

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Upper
from django.utils import timezone

from project.core.fields import EmailField, StringField


class UserManager(BaseUserManager):
    """
    Site-aware user manager that works cleanly with email for public API
    and username for internal Django authentication.

    Uses Django Sites framework as the tenant system.
    """

    def _create_user(
        self,
        email: str,
        site: Site,
        password: str | None = None,
        name: str = "",
        **extra_fields,
    ) -> User:
        """Internal helper to create users with proper site-scoped username."""
        if not email:
            raise ValueError("Email is required")
        if not site:
            raise ValueError("Site is required")

        email = self.normalize_email(email).lower()  # Ensure consistent lowercase
        # Create internal username: "site_id-email"
        # Using site.pk is more stable than domain (domains can change)
        username = f"{site.pk}-{email}"

        user: User = self.model(
            username=username, email=email, site=site, name=name, **extra_fields
        )  # type: ignore[assignment]
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        site: Site,
        password: str | None = None,
        name: str = "",
        **extra_fields,
    ) -> User:
        """Create a regular user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, site, password, name, **extra_fields)

    def create_superuser(
        self,
        email: str,
        site: Site,
        password: str | None = None,
        name: str = "",
        **extra_fields,
    ) -> User:
        """Create a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, site, password, name, **extra_fields)

    def get_by_email_and_site(self, email: str, site: Site) -> User:
        """Public method to get user by email within a site context."""
        return self.get(email__iexact=email, site=site)  # type: ignore[return-value]

    def authenticate_user(self, email: str, site: Site, password: str) -> User | None:
        """Authenticate user with email + site context, using internal username."""
        try:
            user = self.get_by_email_and_site(email, site)
            # Use internal username for Django's authenticate
            from django.contrib.auth import authenticate

            authenticated = authenticate(username=user.username, password=password)
            # Ensure we return a User instance, not AbstractUser
            return authenticated if isinstance(authenticated, User) else None
        except User.DoesNotExist:
            return None


class SiteAwareQuerySet(models.QuerySet):
    """QuerySet that can be filtered by site."""

    def for_site(self, site: Site):
        """Filter queryset for a specific site."""
        return self.filter(site=site)


class SiteAwareManager(models.Manager):
    """Base manager for site-aware models."""

    def get_queryset(self):
        return SiteAwareQuerySet(self.model, using=self._db)

    def for_site(self, site: Site):
        return self.get_queryset().for_site(site)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Multi-tenant User model using Django Sites framework.

    Public Interface: email (what users see/use)
    Internal Interface: username (site_id-email for Django auth)

    Each user belongs to a Site (tenant), enabling true multi-tenancy
    with Django's built-in Sites framework.
    """

    # Site relationship (this IS our tenant)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="users")

    # Internal username field - NEVER exposed to frontend/API
    # Format: "site_id-email" (e.g., "1-user@example.com")
    username = models.CharField(max_length=500, unique=True, db_index=True)

    # Public email field - what users see and use to login
    email = EmailField(verbose_name="email address")
    name = StringField(max_length=500, blank=True, null=True)

    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the admin site.",
        verbose_name="staff_status",
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
        verbose_name="active",
    )

    date_joined = models.DateTimeField(default=timezone.now)

    objects: UserManager = UserManager()

    REQUIRED_FIELDS = ["name", "site"]
    USERNAME_FIELD = "username"  # Django uses username internally

    class Meta:
        db_table = "users"
        constraints = [
            models.CheckConstraint(
                name="user_email_length_check", check=Q(email__length__range=(3, 254))
            ),
            models.CheckConstraint(
                name="user_name_length_check", check=Q(name__length__lte=500)
            ),
            models.CheckConstraint(
                name="user_username_length_check", check=Q(username__length__lte=500)
            ),
            # Email is unique per site, not globally
            models.UniqueConstraint(
                fields=["email", "site"], name="unique_email_per_site"
            ),
            models.UniqueConstraint(Upper("username"), name="user_username_key"),  # type: ignore
        ]

    def __str__(self) -> str:
        return f"{self.email} ({self.site.name})"

    def clean(self):
        """Validate that username matches expected format."""
        if self.username and self.site and self.email:
            expected_username = f"{self.site.pk}-{self.email}"
            if self.username != expected_username:
                raise ValidationError(
                    f"Username must be in format 'site_id-email', got '{self.username}'"
                )

    def save(self, *args, **kwargs):
        # Normalize email consistently
        if self.email:
            from django.contrib.auth.models import BaseUserManager

            self.email = BaseUserManager.normalize_email(self.email).lower()

        # Auto-generate username if not set
        if not self.username and self.site and self.email:
            self.username = f"{self.site.pk}-{self.email}"
        self.full_clean()
        super().save(*args, **kwargs)
