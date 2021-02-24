from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    place = models.ForeignKey("Place", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Place(core_models.TimeStampedModel):

    """ Place Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    viewfinder = models.ForeignKey("users.User", on_delete=models.CASCADE)
    """
    역에 대한 정보도 넣고 싶은데 가까운곳 찾기로.
    구글맵이랑 연동 해야할 듯?
    
    그리고 접근성(airbnb에 있는.)을 추가할지 고려해보자.
    """

    def __str__(self):
        return self.name