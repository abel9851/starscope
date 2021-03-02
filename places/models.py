from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="place_photos")
    place = models.ForeignKey("Place", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Place(core_models.TimeStampedModel):

    """ Place Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    viewfinder = models.ForeignKey(
        "users.User", related_name="places", on_delete=models.CASCADE
    )
    """
    역에 대한 정보도 넣고 싶은데 가까운곳 찾기로.
    구글맵이랑 연동 해야할 듯?
    
    그리고 접근성(airbnb에 있는.)을 추가할지 고려해보자.
    """

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = self.city.title()
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) > 0:
            return all_ratings / len(all_reviews)
        else:
            return 0
