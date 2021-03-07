from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("<int:pk>", views.PlaceDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]