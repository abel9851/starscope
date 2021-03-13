from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from places import models as place_models
from . import models


class PlaceInline(admin.TabularInline):
    model = place_models.Place


# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin Definition """

    inlines = (PlaceInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "supercontentprovider",
                    "login_method",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("supercontentprovider",)

    list_display = (
        "username",
        "first_name",
        "email",
        "is_active",
        "language",
        "currency",
        "is_staff",
        "supercontentprovider",
        "email_verified",
        "email_secret",
        "login_method",
    )