from django.contrib import admin

from .models import Artist

class ArtistModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artist, ArtistModelAdmin)