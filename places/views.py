from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


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


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        city = request.GET.get("city")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                supercontentprovider = form.cleaned_data.get("supercontentprovider")

                filter_args = {}
                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if supercontentprovider is True:
                    filter_args["viewfinder__supercontentprovider"] = True

                qs = models.Place.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                places = paginator.get_page(page)

                return render(
                    request, "places/search.html", {"form": form, "places": places}
                )

        else:
            form = forms.SearchForm(initial={"city": city})

        return render(request, "places/search.html", {"form": form})