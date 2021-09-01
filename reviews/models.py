from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField(verbose_name=_("review"))
    accuracy = models.IntegerField(
        verbose_name=_("Accuracy"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    location = models.IntegerField(
        verbose_name=_("Location"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    cleanliness = models.IntegerField(
        verbose_name=_("Cleanliness"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    satisfaction = models.IntegerField(
        verbose_name=_("Satisfaction"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    user = models.ForeignKey(
        "users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    place = models.ForeignKey(
        "places.Place",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("place"),
    )

    def __str__(self):
        return f"{self.review} - {self.place}"

    def rating_average(self):
        avg = (self.accuracy + self.location + self.cleanliness + self.satisfaction) / 4
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)