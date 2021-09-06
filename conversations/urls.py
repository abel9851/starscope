from django.urls import path
from . import views

app_name = "conversations"


urlpatterns = [
    path(
        "go/<int:placefinder_pk>/<int:place_pk>",
        views.go_conversation,
        name="go",
    ),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
    path("list/", views.conversation_list, name="list"),
]