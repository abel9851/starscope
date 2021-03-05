from django.views.generic import ListView, DetailView
from django.shortcuts import render
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Place
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "places"


class PlaceDetail(DetailView):

    """ PlaceDetail Definition """

    model = models.Place
