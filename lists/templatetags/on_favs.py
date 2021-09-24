from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, place):
    user = context.request.user
    if user.is_authenticated:
        the_list = list_models.List.objects.get_or_none(
            user=user, name="My Favorite Places"
        )
        if the_list is not None:
            return place in the_list.places.all()
        else:
            return False
    else:
        return False
