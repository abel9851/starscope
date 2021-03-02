from django.contrib import admin
from django.utils.html import mark_safe
from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):

    """ Place Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                ),
            },
        ),
        (
            "Details",
            {"fields": ("viewfinder",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "address",
        "viewfinder",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "viewfinder__supercontentprovider",
        "city",
        "country",
    )

    raw_id_fields = ("viewfinder",)

    search_fields = ("city", "^viewfinder__username")

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src= "{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
