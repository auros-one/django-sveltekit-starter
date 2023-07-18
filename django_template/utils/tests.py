from django import forms
from hypothesis import given
from hypothesis.extra.django import from_field

from .fields import SlugField


@given(slug=from_field(SlugField(blank=True)))
def test_slugfield_form(slug):
    class SlugFieldForm(forms.Form):
        slug = SlugField(blank=True).formfield()

    form = SlugFieldForm(data={"slug": slug})
    assert form.is_valid()
