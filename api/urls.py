from django.urls import path, include
from rest_framework import routers
from .views import ExtractData

router = routers.DefaultRouter()
router.register(r'extract', ExtractData, basename="extract")
# router.register(r'get_news', NewsLookupSet, basename="get_news")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]