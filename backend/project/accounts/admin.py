from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users in the admin.
    Handles site-aware user creation with email + site → username generation.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Enter a strong password for the user."),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("email", "name", "site")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        site = self.cleaned_data.get("site")

        if email and site:
            # Check if email already exists in this site
            if User.objects.filter(email__iexact=email, site=site).exists():
                raise ValidationError(
                    _("A user with this email already exists in this site.")
                )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Ensure username is generated even with commit=False (for tests)
        if not user.username and user.site and user.email:
            user.username = f"{user.site.pk}-{user.email}"

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form for updating users in the admin.
    Includes all fields but replaces password with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        site = self.cleaned_data.get("site")

        if email and site:
            # Check if email already exists in this site (excluding current user)
            existing_users = User.objects.filter(email__iexact=email, site=site)
            if self.instance:
                existing_users = existing_users.exclude(pk=self.instance.pk)

            if existing_users.exists():
                raise ValidationError(
                    _("A user with this email already exists in this site.")
                )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # Update username if email or site changed
        if user.site and user.email:
            expected_username = f"{user.site.pk}-{user.email}"
            if user.username != expected_username:
                user.username = expected_username

        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """
    Custom admin authentication form that accepts email instead of username.
    Converts email to internal username format for authentication.
    """

    username = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )

    def clean(self):
        email = self.cleaned_data.get("username")  # Actually email
        password = self.cleaned_data.get("password")

        if email is not None and password:
            # Get the current site from request context
            request = getattr(self, "request", None)
            if not request or not hasattr(request, "site"):
                # Fallback: try to find user by email across all sites
                try:
                    user = User.objects.filter(email__iexact=email).first()
                    if user:
                        site = user.site
                    else:
                        raise forms.ValidationError(
                            _("Please enter a correct email and password."),
                            code="invalid_login",
                        )
                except User.DoesNotExist:
                    raise forms.ValidationError(
                        _("Please enter a correct email and password."),
                        code="invalid_login",
                    )
            else:
                site = request.site

            # Use our custom authentication method
            user_cache = User.objects.authenticate_user(email, site, password)

            if user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct email and password."),
                    code="invalid_login",
                )
            else:
                self.user_cache = user_cache  # type: ignore
                assert self.user_cache is not None  # For type checker
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomAdminSite(AdminSite):
    """
    Custom admin site that uses email-based authentication.
    """

    site_header = "Django Administration"
    site_title = "Django site admin"
    index_title = "Welcome to Django administration"
    login_form = EmailAuthenticationForm

    def login(self, request, extra_context=None):
        """
        Override login to attach site context to the authentication form.
        """
        response = super().login(request, extra_context)

        # Attach request to form for site context
        if hasattr(self, "_registry") and request.method == "POST":
            form = getattr(request, "_admin_login_form", None)
            if form:
                form.request = request

        return response


# Create custom admin site instance
admin_site = CustomAdminSite(name="admin")

# Unregister Site from default admin (Django's sites app registers it automatically)
try:
    admin.site.unregister(Site)
except NotRegistered:
    pass  # Site wasn't registered, which is fine


# Custom Site admin for better multi-tenant management
@admin.register(Site, site=admin_site)
class SiteAdmin(admin.ModelAdmin):
    """
    Enhanced Site admin for multi-tenant management.
    """

    list_display = ("domain", "name", "id")
    list_display_links = ("domain", "name")
    search_fields = ("domain", "name")
    ordering = ("domain",)

    fieldsets = (
        (
            None,
            {
                "fields": ("domain", "name"),
                "description": "Each site represents a tenant in the multi-tenant system. "
                "Users are isolated by site.",
            },
        ),
    )


@admin.register(User, site=admin_site)
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin that shows email-friendly fields and uses our custom forms.
    """

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "name", "site", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active", "site", "date_joined")
    search_fields = ("email", "name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Site"), {"fields": ("site",)}),
        (
            _("Internal"),
            {"fields": ("username",), "classes": ("collapse",)},
        ),  # Hide username by default
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "site", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("date_joined", "last_login", "username")


# Register the User model with the custom admin site

admin.site.unregister(Group)
