from django.urls import path, include
from rest_framework import routers
from .views import ExtractData, SiteConfigViewSet

router = routers.DefaultRouter()
router.register(r'packages', SiteConfigViewSet, basename="packages")
router.register(r'extract', ExtractData, basename="extract")
# router.register(r'get_news', NewsLookupSet, basename="get_news")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]