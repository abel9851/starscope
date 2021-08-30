from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:place>/", views.create_review, name="create"),
    path("update/<int:place>/<int:comment>", views.update_review, name="update"),
    path("delete/<int:place>/<int:comment>", views.delete_review, name="delete"),
]
