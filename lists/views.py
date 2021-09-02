from django.contrib.messages.api import error
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from places import models as place_models
from . import models


def save_place(request, place_pk):
    place = place_models.Place.objects.get_or_none(pk=place_pk)
    if place is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favorite Places"
        )
        messages.success(request, _("My Fovorite saved"))
        the_list.places.add(place)

    else:
        messages.error(request, _("Place does not exist"))

    return redirect(reverse("places:detail", kwargs={"pk": place_pk}))
