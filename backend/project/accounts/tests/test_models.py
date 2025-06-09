import pytest
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..models import User


@pytest.mark.django_db
class TestUser:
    def test_create_user(self, site):
        user = User.objects.create_user(
            email="piet@example.com",
            site=site,
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        assert user.email == "piet@example.com"
        assert user.site == site
        assert user.username == f"{site.pk}-piet@example.com"
        assert user.name == "Piet Mondrian"
        assert not user.is_staff
        assert not user.is_superuser
        # Password should be hashed.
        assert user.password != "correcthorsebatterystaple"

    def test_create_superuser(self, site):
        user = User.objects.create_superuser(
            email="piet@example.com",
            site=site,
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        assert user.email == "piet@example.com"
        assert user.site == site
        assert user.username == f"{site.pk}-piet@example.com"
        assert user.name == "Piet Mondrian"
        assert user.is_staff
        assert user.is_superuser
        # Password should be hashed.
        assert user.password != "correcthorsebatterystaple"

    def test_get_user_by_case_insensitive_email(self, site):
        user = User.objects.create_user(
            email="fRoMThENiNEtiEs@example.com",
            site=site,
            name="l33t h4x0r",
            password="trustno1",
        )
        # Test our new site-aware method
        found_user = User.objects.get_by_email_and_site(
            "fromthenineties@example.com", site
        )
        assert found_user == user

    def test_email_case_insensitively_unique_per_site(self, site):
        """Test that emails are unique within a site but can exist across sites."""
        User.objects.create_user(
            email="piet@example.com",
            site=site,
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )

        # Same email in same site should fail (different case but normalized to same)
        # Since we normalize emails to lowercase, this will hit BOTH constraints:
        # 1. The email+site unique constraint
        # 2. The username unique constraint (since username is site_id-email)
        with pytest.raises(
            (
                IntegrityError,
                ValidationError,
            )  # Accept either IntegrityError or ValidationError
        ), transaction.atomic():
            User.objects.create_user(
                email="Piet@example.com",  # Different case but will be normalized to lowercase
                site=site,
                name="Piet Mondrian",
                password="correcthorsebatterystaple",
            )

        # Exactly the same email in same site should also fail
        with pytest.raises((IntegrityError, ValidationError)), transaction.atomic():
            User.objects.create_user(
                email="piet@example.com",
                site=site,
                name="Piet Mondrian",
                password="correcthorsebatterystaple",
            )

    def test_email_can_exist_in_different_sites(self):
        """Test that same email can exist in different sites."""
        site1 = Site.objects.create(domain="site1.example.com", name="Site 1")
        site2 = Site.objects.create(domain="site2.example.com", name="Site 2")

        # Create user with same email in different sites
        user1 = User.objects.create_user(
            email="shared@example.com",
            site=site1,
            name="User One",
            password="password1",
        )

        user2 = User.objects.create_user(
            email="shared@example.com",
            site=site2,
            name="User Two",
            password="password2",
        )

        # Both should exist with different usernames
        assert user1.email == user2.email
        assert user1.site != user2.site
        assert user1.username != user2.username
        assert user1.username == f"{site1.pk}-shared@example.com"
        assert user2.username == f"{site2.pk}-shared@example.com"

    def test_str(self, site):
        user = User.objects.create_user(
            email="piet@example.com",
            site=site,
            name="Piet Mondrian",
            password="correcthorsebatterystaple",
        )
        # Updated assertion for new __str__ format: "email (site_name)"
        assert str(user) == f"piet@example.com ({site.name})"

    def test_username_auto_generation(self, site):
        """Test that username is automatically generated from site and email."""
        user = User(email="auto@example.com", site=site, name="Auto User")
        user.set_password("password")
        user.save()

        expected_username = f"{site.pk}-auto@example.com"
        assert user.username == expected_username

    def test_authenticate_user_method(self, site):
        """Test the site-aware authenticate_user method."""
        user = User.objects.create_user(
            email="auth@example.com", site=site, password="authpassword"
        )

        # Should authenticate with correct credentials
        authenticated = User.objects.authenticate_user(
            "auth@example.com", site, "authpassword"
        )
        assert authenticated == user

        # Should fail with wrong password
        not_authenticated = User.objects.authenticate_user(
            "auth@example.com", site, "wrongpassword"
        )
        assert not_authenticated is None

        # Should fail with wrong site
        other_site = Site.objects.create(domain="other.example.com", name="Other Site")
        not_authenticated = User.objects.authenticate_user(
            "auth@example.com", other_site, "authpassword"
        )
        assert not_authenticated is None
