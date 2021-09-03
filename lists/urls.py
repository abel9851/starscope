from django.urls import path
from . import views

app_name = "lists"


urlpatterns = [
    path("toggle/<int:place_pk>/", views.toggle_place, name="toggle-place"),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]