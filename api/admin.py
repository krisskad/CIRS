from django.contrib import admin
from django.contrib import admin
from api.models import SiteConfig, Extraction


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('trial_limit', 'standard_limit', 'business_limit')

    def has_add_permission(self, request): # Here
        return not SiteConfig.objects.exists()

@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_term', 'amazon')