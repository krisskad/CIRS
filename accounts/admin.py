from django.contrib import admin
from django.contrib import admin
from accounts.models import UserAccount, Packages


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'coins', 'date_joined')


@admin.register(Packages)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'search_limit', )

    def has_add_permission(self, request): # Here
        return not Packages.objects.exists()
