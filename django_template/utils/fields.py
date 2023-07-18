from django import forms
from django.core import validators
from django.db import models


class StringField(models.CharField):
    """A text field that uses a single line form widget.

    In Postgres it's almost always better to use a text field rather than a varchar:
    https://stackoverflow.com/a/4849030/625910

    Keep in mind that max_length isn't enforced at the database level, so if it's
    needed, you must add a check constraint to the model.
    """

    description = "String"

    def __init__(self, *args, **kwargs):
        self.has_max_length = True
        if "max_length" not in kwargs:
            self.has_max_length = False
            # Django demands some value, so give it something big.
            kwargs["max_length"] = int(1e20)
        super().__init__(*args, **kwargs)
        if not self.has_max_length:
            self.validators.remove(validators.MaxLengthValidator(self.max_length))

    def db_type(self, connection) -> str:
        return "text"

    def formfield(self, **kwargs):
        if not self.has_max_length:
            kwargs["max_length"] = None
        return super().formfield(**kwargs)


class EmailField(StringField):
    """Replacement for django.db.models.EmailField, using the text type."""

    default_validators = [validators.validate_email]
    description = "Email"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 254)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{**kwargs, "widget": forms.EmailInput})


class SlugField(StringField):
    """Replacement for django.db.models.SlugField, using the text type."""

    default_validators = [validators.validate_unicode_slug]
    description = "Slug"

    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": forms.SlugField, **kwargs})
