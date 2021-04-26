from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="JP").formfield()
    supercontentprovider = forms.BooleanField(required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

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
