from django.contrib import admin
from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):

    """ Place Admin Definition """

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass