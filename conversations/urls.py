from django.urls import path
from . import views

app_name = "conversations"


urlpatterns = [
    path(
        "go/<int:palcefinder_pk>/<int:place_pk>",
        views.go_conversation,
        name="go",
    ),
]