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
    def test_user_creation_form(self, data, errors):
        form = UserCreationForm(data)
        assert form.is_valid() is not bool(errors)
        assert errors == form.errors
        if not errors:
            user = form.save(commit=False)
            # Password should be hashed.
            assert user.password not in {data["password1"], data["password2"]}

    def test_user_creation_form_saves(self):
        form = UserCreationForm(
            data={
                "email": "piet@example.com",
                "name": "Piet Mondrian",
                "password1": "correcthorsebatterystaple",
                "password2": "correcthorsebatterystaple",
            }
        )
        assert form.is_valid()
        user = form.save()
        # Password should be hashed.
        assert user.password != "correcthorsebatterystaple"
