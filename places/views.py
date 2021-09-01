from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Place
    paginate_by = 12
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


class EditPlaceView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Place
    template_name = "places/place_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "address",
    )

    def get_object(self, queryset=None):
        place = super().get_object(queryset=queryset)
        if place.viewfinder.pk != self.request.user.pk:
            raise Http404()
        return place


def delete_place(request, place_pk):
    user = request.user

    try:
        place = models.Place.objects.get(pk=place_pk)
        if place.viewfinder.pk != user.pk:
            messages.error(request, _("You can't delete this place"))

        else:
            messages.success(request, _("Place Deleted"))
            place.delete()

        return redirect(reverse("core:home"))

    except models.Place.DoesNotExist:
        redirect(reverse("core:home"))


class PlacePhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Place
    template_name = "places/Place_photos.html"

    def get_object(self, queryset=None):
        place = super().get_object(queryset=queryset)
        if place.viewfinder.pk != self.request.user.pk:
            raise Http404()
        return place


@login_required
def delete_photo(request, place_pk, photo_pk):
    user = request.user
    try:
        place = models.Place.objects.get(pk=place_pk)
        if place.viewfinder.pk != user.pk:
            messages.error(request, _("Can't delete that photo"))
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, _("photo deleted"))
        return redirect(reverse("places:photos", kwargs={"pk": place_pk}))
    except models.Place.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    pk_url_kwarg = "photo_pk"
    template_name = "places/Photo_edit.html"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        place_pk = self.kwargs.get("place_pk")
        return reverse("places:photos", kwargs={"pk": place_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "places/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, _("Photo Uploaded"))
        return redirect(reverse("places:photos", kwargs={"pk": pk}))


class CreatePlaceView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreatePlaceForm
    template_name = "places/place_create.html"

    def form_valid(self, form):
        place = form.save()
        place.viewfinder = self.request.user
        place.save()
        form.save_m2m()
        messages.success(self.request, _("Place Created"))
        return redirect(reverse("places:detail", kwargs={"pk": place.pk}))