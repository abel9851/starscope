from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField(verbose_name="レビュー")
    accuracy = models.IntegerField(verbose_name="正確性")
    location = models.IntegerField(verbose_name="位置")
    cleanliness = models.IntegerField(verbose_name="淸潔")
    satisfaction = models.IntegerField(verbose_name="満足度")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review} - {self.place}"
