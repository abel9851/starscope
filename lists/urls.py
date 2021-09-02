from django.urls import path
from . import views

app_name = "lists"


urlpatterns = [
    path("list-adds/<int:place_pk>/", views.save_place, name="save-place"),
]