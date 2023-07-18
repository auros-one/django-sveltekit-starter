from __future__ import annotations

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q
from django.db.models.functions import Upper
from django.utils import timezone

from django_template.utils.fields import EmailField, StringField


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username: str | None) -> User:  # type: ignore[override]
        """Return a user by its case-insensitive username field.

        This is called in various places, for example when authenticating.
        """
        username_field = self.model.USERNAME_FIELD  # type: ignore[attr-defined]
        return self.get(
            **{f"{username_field}__iexact": username}  # type: ignore[return-value]
        )

    def create_user(self, email: str, name: str, password: str | None = None) -> User:
        """Create and save a user."""
        user: User = self.model(
            email=self.normalize_email(email), name=name
        )  # type: ignore[assignment]
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, name: str, password: str | None = None
    ) -> User:
        """Create and save a user with superuser status."""
        user: User = self.create_user(email, password=password, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField(verbose_name="email address")
    name = StringField(max_length=500)

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

    objects = UserManager()

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = "email"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="user_email_length_check", check=Q(email__length__range=(3, 254))
            ),
            models.CheckConstraint(
                name="user_name_length_check", check=Q(name__length__lte=500)
            ),
            models.UniqueConstraint(Upper("email"), name="user_email_key"),  # type: ignore
        ]

    def __str__(self) -> str:
        return self.name
