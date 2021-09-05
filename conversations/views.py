from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.utils.translation import gettext_lazy as _
from users import models as user_models
from . import models


# Create your views here.


def go_conversation(request, placefinder_pk, place_pk):
    user_one = user_models.User.objects.get_or_none(pk=request.user.pk)
    user_two = user_models.User.objects.get_or_none(pk=placefinder_pk)
    if user_one is not None and user_two is not None:
        if user_one == user_two:
            messages.error(request, _("You can't this"))
            redirect(reverse("places:detail", kwargs={"pk": place_pk}))
        else:
            try:
                conversation = models.Conversation.objects.get(
                    Q(participants=user_two) & Q(participants=user_one)
                )

            except models.Conversation.DoesNotExist:
                conversation = models.Conversation.objects.create(participants=user_two)
                conversation.participants.add(user_one)
