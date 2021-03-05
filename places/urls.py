from django.urls import path
from . import views

app_name = "place"

urlpatterns = [path("<int:pk>", views.PlaceDetail.as_view(), name="detail")]
