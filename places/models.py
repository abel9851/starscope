from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from core import models as core_models
from django.urls import reverse


class Photo(core_models.TimeStampedModel):

    """ Photo Model definition """

    caption = models.CharField(_("caption"), max_length=80)
    file = models.ImageField(_("file"), upload_to="place_photos")
    place = models.ForeignKey(
        "Place",
        related_name="photos",
        on_delete=models.CASCADE,
        verbose_name=_("place"),
    )

    def __str__(self):
        return self.caption


class Place(core_models.TimeStampedModel):

    """ Place Model Definition """

    name = models.CharField(_("name"), max_length=140)
    description = models.TextField(
        _("description"),
    )
    country = CountryField(
        _("country"),
    )
    city = models.CharField(_("city"), max_length=80)
    address = models.CharField(_("address"), max_length=140)
    viewfinder = models.ForeignKey(
        "users.User",
        related_name="places",
        on_delete=models.CASCADE,
        verbose_name=_("viewfinder"),
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

    def get_absolute_url(self):
        return reverse("places:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) > 0:
            return round(all_ratings / len(all_reviews), 2)
        else:
            return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos
