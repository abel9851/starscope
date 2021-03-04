from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Place
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "places"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context