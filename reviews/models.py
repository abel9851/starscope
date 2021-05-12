from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField(verbose_name="レビュー")
    accuracy = models.IntegerField(
        verbose_name="正確性", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        verbose_name="位置", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        verbose_name="淸潔", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    satisfaction = models.IntegerField(
        verbose_name="満足度", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        "places.Place", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.place}"

    def rating_average(self):
        avg = (self.accuracy + self.location + self.cleanliness + self.satisfaction) / 4
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)