from django.contrib import admin
from django.contrib import admin
from api.models import Extraction


@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_term', 'amazon')