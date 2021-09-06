from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User",
        related_name="conversations",
        blank=True,
        verbose_name=_("participants"),
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)

        if usernames == []:
            return "No users"
        else:
            return " & ".join(usernames) + " conversation"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField(
        _("message"),
    )
    user = models.ForeignKey(
        "users.User",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    conversation = models.ForeignKey(
        "Conversation",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("conversation"),
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
