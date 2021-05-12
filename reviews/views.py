from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from places import models as place_models
from . import models as review_models
from . import forms


@login_required
def form_review(request, place):
    place = place_models.Place.objects.get_or_none(pk=place)
    form = forms.CreateReviewForm()
    return render(request, "reviews/form.html", {"form": form, "place": place})


@login_required
def create_review(request, place):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        place = place_models.Place.objects.get_or_none(pk=place)
        if not place:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, "Place reviewed")
            return redirect(reverse("places:detail", kwargs={"pk": place.pk}))


@login_required
def update_review(request, place, comment):
    review = get_object_or_404(review_models.Review, pk=comment)
    place = place_models.Place.objects.get_or_none(pk=place)

    if request.user != review.user:
        messages.error(request, "You can't")
        return redirect(reverse("places:detail", kwargs={"pk": place.pk}))

    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST, instance=review)
        if form.is_valid():
            messages.success(request, "Review updated")
            review = form.save()
            review.save()
            return redirect(reverse("places:detail", kwargs={"pk": place.pk}))
    else:
        form = forms.CreateReviewForm(instance=review)
    return render(request, "reviews/update.html", {"form": form})


@login_required
def delete_review(request, place, comment):
    review = get_object_or_404(review_models.Review, pk=comment)
    place = place_models.Place.objects.get_or_none(pk=place)

    if request.user != review.user:
        messages.error(request, "You can't")
        return redirect(reverse("places:detail", kwargs={"pk": place.pk}))

    messages.success(request, "Review deleted")
    review.delete()
    return redirect(reverse("places:detail", kwargs={"pk": place.pk}))
