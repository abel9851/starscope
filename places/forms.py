from django import forms
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="JP").formfield()
    supercontentprovider = forms.BooleanField(required=False)