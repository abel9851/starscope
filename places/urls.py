from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("create/", views.CreatePlaceView.as_view(), name="create"),
    path("<int:pk>/", views.PlaceDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditPlaceView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.PlacePhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:place_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:place_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
