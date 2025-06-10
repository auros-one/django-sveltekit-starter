import pytest

from ..admin import UserCreationForm


@pytest.mark.django_db
class TestUserCreationForm:
    @pytest.mark.parametrize(
        "data, errors",
        [
            (
                {
                    "email": "piet@example.com",
                    "name": "Piet Mondrian",
                    "password1": "correcthorsebatterystaple",
                    "password2": "correcthorsebatterystaple",
                },
                {},
            ),
            (
                {
                    "email": "piet@example.com",
                    "name": "Piet Mondrian",
                    "password1": "correcthorsebatterystaple",
                    "password2": "incorrecthorsebatterystaple",
                },
                {"password2": ["The two password fields didn't match."]},
            ),
        ],
    )
    def test_user_creation_form(self, data, errors, site):
        # Add site to form data
        data_with_site = {**data, "site": site.pk}
        form = UserCreationForm(data_with_site)

        # Check form validity
        assert form.is_valid() is not bool(errors)

        # If we expect errors, check them
        if errors:
            for field, expected_errors in errors.items():
                assert field in form.errors
                assert expected_errors == form.errors[field]

        # If form is valid, test password hashing
        if not errors:
            user = form.save(commit=False)
            # Password should be hashed
            assert user.password not in {data["password1"], data["password2"]}
            # Should have proper site and username
            assert user.site == site
            assert user.username == f"{site.pk}-{data['email']}"

    def test_user_creation_form_saves(self, site):
        form = UserCreationForm(
            data={
                "email": "piet@example.com",
                "name": "Piet Mondrian",
                "site": site.pk,
                "password1": "correcthorsebatterystaple",
                "password2": "correcthorsebatterystaple",
            }
        )
        assert form.is_valid()
        user = form.save()

        # Check user was created correctly
        assert user.email == "piet@example.com"
        assert user.name == "Piet Mondrian"
        assert user.site == site
        assert user.username == f"{site.pk}-piet@example.com"
        # Password should be hashed
        assert user.password != "correcthorsebatterystaple"

    def test_user_creation_form_requires_site(self):
        """Test that form requires site field."""
        form = UserCreationForm(
            data={
                "email": "nositeuser@example.com",
                "name": "No Site User",
                "password1": "correcthorsebatterystaple",
                "password2": "correcthorsebatterystaple",
                # Missing site field
            }
        )
        assert not form.is_valid()
        assert "site" in form.errors

    def test_user_creation_form_prevents_duplicate_email_in_site(self, site):
        """Test that form prevents duplicate emails within same site."""
        # Create existing user
        from ..models import User

        User.objects.create_user(
            email="duplicate@example.com", site=site, password="existing"
        )

        # Try to create another user with same email in same site
        form = UserCreationForm(
            data={
                "email": "duplicate@example.com",
                "name": "Duplicate User",
                "site": site.pk,
                "password1": "correcthorsebatterystaple",
                "password2": "correcthorsebatterystaple",
            }
        )
        assert not form.is_valid()

        # The error could be on the email field or as a non-field error
        assert not form.is_valid()
        error_found = False

        # Check if error is on email field
        if "email" in form.errors:
            assert "already exists" in str(form.errors["email"]).lower()
            error_found = True

        # Check if error is in non-field errors
        if "__all__" in form.errors:
            assert "already exists" in str(form.errors["__all__"]).lower()
            error_found = True

        assert error_found, f"Expected duplicate email error but got: {form.errors}"
