from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from places import models as place_models
from users.mixins import LoggedInOnlyView
from . import models


def toggle_place(request, place_pk):
    action = request.GET.get("action", None)
    place = place_models.Place.objects.get_or_none(pk=place_pk)
    if place is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favorite Places"
        )
        if action == "add":
            messages.success(request, _("My Fovorite saved"))
            the_list.places.add(place)
        elif action == "remove":
            messages.success(request, _("My Fovorite removed"))
            the_list.places.remove(place)
        else:
            messages.error(request, _("You can't this"))
            return redirect(reverse("places:detail", kwargs={"pk": place_pk}))

    else:
        messages.error(request, _("Place does not exist"))

    return redirect(reverse("places:detail", kwargs={"pk": place_pk}))


class SeeFavsView(LoggedInOnlyView, TemplateView):

    template_name = "lists/list_detail.html"
