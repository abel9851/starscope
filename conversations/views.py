from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from users import models as user_models
from users.mixins import LoggedInOnlyView
from . import models


@login_required
def go_conversation(request, placefinder_pk, place_pk):

    """ Conversation Create & redirect definition """

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
                conversation = models.Conversation.objects.create()
                conversation.participants.add(user_one, user_two)
            return redirect(
                reverse("conversations:detail", kwargs={"pk": conversation.pk})
            )


class ConversationDetailView(LoggedInOnlyView, View):

    """ Conversation Detail Definition """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if self.request.user not in conversation.participants.all():
            messages.error(self.request, _("You can't access"))
            redirect(reverse("core:home"))
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        if message is not None:
            conversation = models.Conversation.objects.get_or_none(pk=pk)
            if not conversation:
                raise Http404()
            if self.request.user not in conversation.participants.all():
                messages.error(self.request, _("You can't access"))
                redirect(reverse("core:home"))
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))


@login_required
def conversation_list(request):
    user = request.user
    conversation_list = models.Conversation.objects.filter(participants=user)
    return render(
        request,
        "conversations/conversation_list.html",
        {"conversation_list": conversation_list},
    )
