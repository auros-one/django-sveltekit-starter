from unittest.mock import Mock

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.sites.models import Site

from ..admin import EmailAuthenticationForm, UserAdmin, UserChangeForm, UserCreationForm
from ..models import User


@pytest.mark.django_db
class TestAdminAuthentication:
    """Test suite for Django admin authentication with email-based login."""

    def test_email_authentication_form_accepts_email(self, user):
        """Test that admin login form accepts email instead of username."""
        form_data = {
            "username": user.email,  # Form field is called 'username' but accepts email
            "password": "a-super-strong-password-145338-@!#&",
        }

        form = EmailAuthenticationForm(data=form_data)

        # Mock request with site context
        mock_request = Mock()
        mock_request.site = user.site
        form.request = mock_request

        assert form.is_valid()
        assert form.user_cache == user

    def test_email_authentication_form_site_aware(self):
        """Test that admin login respects site boundaries."""
        site1 = Site.objects.create(domain="admin1.test", name="Admin Site 1")
        site2 = Site.objects.create(domain="admin2.test", name="Admin Site 2")

        email = "admin@example.com"
        password = "admin-password-123!"

        user1 = User.objects.create_user(email=email, site=site1, password=password)
        user2 = User.objects.create_user(email=email, site=site2, password=password)

        # Login should find user1 when in site1 context
        form_data = {"username": email, "password": password}
        form = EmailAuthenticationForm(data=form_data)

        mock_request = Mock()
        mock_request.site = site1
        form.request = mock_request

        assert form.is_valid()
        assert form.user_cache == user1

        # Login should find user2 when in site2 context
        form = EmailAuthenticationForm(data=form_data)
        mock_request.site = site2
        form.request = mock_request

        assert form.is_valid()
        assert form.user_cache == user2

    def test_email_authentication_form_fallback_without_site(self):
        """Test that admin login works even without site middleware (fallback mode)."""
        site = Site.objects.create(domain="fallback.test", name="Fallback Site")
        email = "fallback@example.com"
        password = "fallback-password-123!"

        user = User.objects.create_user(email=email, site=site, password=password)

        form_data = {"username": email, "password": password}
        form = EmailAuthenticationForm(data=form_data)
        # Don't set request.site to simulate missing middleware

        assert form.is_valid()
        assert form.user_cache == user

    def test_email_authentication_form_invalid_credentials(self, user):
        """Test that admin login fails with wrong credentials."""
        form_data = {"username": user.email, "password": "wrong-password"}

        form = EmailAuthenticationForm(data=form_data)
        mock_request = Mock()
        mock_request.site = user.site
        form.request = mock_request

        assert not form.is_valid()
        assert "Please enter a correct email and password." in str(form.errors)

    def test_email_authentication_form_nonexistent_user(self, site):
        """Test that admin login fails for non-existent users."""
        form_data = {"username": "nonexistent@example.com", "password": "any-password"}

        form = EmailAuthenticationForm(data=form_data)
        mock_request = Mock()
        mock_request.site = site
        form.request = mock_request

        assert not form.is_valid()
        assert "Please enter a correct email and password." in str(form.errors)


@pytest.mark.django_db
class TestAdminUserForms:
    """Test suite for Django admin user creation and change forms."""

    def test_user_creation_form_creates_site_aware_user(self, site):
        """Test that admin user creation form works with site context."""
        form_data = {
            "email": "newadmin@example.com",
            "name": "New Admin",
            "site": site.pk,
            "password1": "super-strong-admin-password!",
            "password2": "super-strong-admin-password!",
        }

        form = UserCreationForm(data=form_data)
        assert form.is_valid(), f"Form errors: {form.errors}"

        user = form.save()
        assert user.email == "newadmin@example.com"
        assert user.site == site
        assert user.username == f"{site.pk}-newadmin@example.com"
        assert user.check_password("super-strong-admin-password!")

    def test_user_creation_form_prevents_duplicate_email_in_site(self, site):
        """Test that admin user creation prevents duplicate emails in same site."""
        # Create existing user
        User.objects.create_user(
            email="existing@example.com", site=site, password="existing123"
        )

        # Try to create another user with same email in same site
        form_data = {
            "email": "existing@example.com",
            "name": "Duplicate User",
            "site": site.pk,
            "password1": "password123!",
            "password2": "password123!",
        }

        form = UserCreationForm(data=form_data)
        assert not form.is_valid()
        # Check that there's some validation error (could be in email field or non_field_errors)
        assert (
            form.errors
        ), f"Expected validation errors but got none. Form data: {form_data}"
        # Either email field has error or there are non-field errors
        has_email_error = "email" in form.errors and any(
            "already exists" in str(error) for error in form.errors["email"]
        )
        has_general_error = "__all__" in form.errors or any(
            "email" in str(errors).lower() for errors in form.errors.values()
        )
        assert (
            has_email_error or has_general_error
        ), f"Expected email duplicate error but got: {form.errors}"

    def test_user_creation_form_allows_same_email_different_sites(self):
        """Test that admin user creation allows same email in different sites."""
        site1 = Site.objects.create(domain="site1.admin", name="Site 1")
        site2 = Site.objects.create(domain="site2.admin", name="Site 2")

        email = "shared@example.com"

        # Create user in site1
        User.objects.create_user(email=email, site=site1, password="password1")

        # Create user with same email in site2 - should succeed
        form_data = {
            "email": email,
            "name": "Site 2 User",
            "site": site2.pk,
            "password1": "password123!",
            "password2": "password123!",
        }

        form = UserCreationForm(data=form_data)
        assert form.is_valid()

        user = form.save()
        assert user.email == email
        assert user.site == site2

    def test_user_creation_form_password_mismatch(self, site):
        """Test that admin user creation validates password confirmation."""
        form_data = {
            "email": "mismatch@example.com",
            "name": "Mismatch User",
            "site": site.pk,
            "password1": "password123!",
            "password2": "different-password!",
        }

        form = UserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "The two password fields didn't match." in form.errors["password2"]

    def test_user_change_form_updates_user(self, user):
        """Test that admin user change form works correctly."""
        new_email = "updated@example.com"
        expected_username = f"{user.site.pk}-{new_email}"

        form_data = {
            "email": new_email,
            "name": "Updated Name",
            "site": user.site.pk,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
            "groups": [],
            "user_permissions": [],
            "password": user.password,  # Include the hashed password
            "username": expected_username,  # Use the expected new username
        }

        form = UserChangeForm(data=form_data, instance=user)
        assert form.is_valid(), f"Form errors: {form.errors}"

        updated_user = form.save()
        assert updated_user.email == new_email
        assert updated_user.name == "Updated Name"
        assert updated_user.username == expected_username

    def test_user_change_form_prevents_duplicate_email(self, user, same_site_user):
        """Test that admin user change form prevents duplicate emails in same site."""
        form_data = {
            "email": same_site_user.email,  # Try to use another user's email
            "name": user.name,
            "site": user.site.pk,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }

        form = UserChangeForm(data=form_data, instance=user)
        assert not form.is_valid()
        # Check that there's some validation error about email duplication
        assert (
            form.errors
        ), f"Expected validation errors but got none. Form data: {form_data}"
        has_email_error = "email" in form.errors and any(
            "already exists" in str(error) for error in form.errors["email"]
        )
        has_general_error = "__all__" in form.errors or any(
            "email" in str(errors).lower() for errors in form.errors.values()
        )
        assert (
            has_email_error or has_general_error
        ), f"Expected email duplicate error but got: {form.errors}"

    def test_user_admin_configuration(self):
        """Test that UserAdmin is properly configured for multi-tenant use."""
        admin = UserAdmin(User, AdminSite())

        # Check that forms are set correctly
        assert admin.form == UserChangeForm
        assert admin.add_form == UserCreationForm

        # Check that site field is included in admin
        assert "site" in admin.list_display
        assert "site" in admin.list_filter

        # Check that username is hidden by default (collapsed section)
        internal_fieldset = None
        for fieldset in admin.fieldsets:
            if fieldset[0] == "Internal":
                internal_fieldset = fieldset
                break

        assert internal_fieldset is not None
        assert "username" in internal_fieldset[1]["fields"]
        assert "collapse" in internal_fieldset[1]["classes"]

    def test_user_admin_readonly_fields(self):
        """Test that certain fields are read-only in admin."""
        admin = UserAdmin(User, AdminSite())

        readonly_fields = admin.readonly_fields
        assert "username" in readonly_fields  # Username should be read-only
        assert "date_joined" in readonly_fields
        assert "last_login" in readonly_fields

    def test_user_admin_add_fieldsets(self):
        """Test that add user form includes site field."""
        admin = UserAdmin(User, AdminSite())

        add_fieldset = admin.add_fieldsets[0]
        fields = add_fieldset[1]["fields"]

        assert "email" in fields
        assert "site" in fields  # Critical for multi-tenancy
        assert "password1" in fields
        assert "password2" in fields
