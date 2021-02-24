from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):

    """ List Model definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    places = models.ManyToManyField("places.Place", blank=True)

    def __str__(self):
        return self.name