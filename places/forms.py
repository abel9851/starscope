from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    city = forms.CharField(
        initial="Anywhere",
        label=_("city"),
        widget=forms.TextInput(attrs={"place_holder": _("city")}),
    )
    country = CountryField(default="JP").formfield(
        label=_("country"),
    )
    supercontentprovider = forms.BooleanField(
        required=False,
        label=_("supercontentprovider"),
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )
        widgets = {
            "caption": forms.TextInput(attrs={"place_holder": _("caption")}),
        }

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        place = models.Place.objects.get(pk=pk)
        photo.place = place
        photo.save()


class CreatePlaceForm(forms.ModelForm):
    class Meta:
        model = models.Place
        fields = (
            "name",
            "description",
            "country",
            "city",
            "address",
        )

    def save(self, *args, **kwargs):
        place = super().save(commit=False)
        return place
