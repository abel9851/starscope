from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    accuracy = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    satisfaction = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "location",
            "cleanliness",
            "satisfaction",
        )

    def save(self):
        reviews = super().save(commit=False)
        return reviews
