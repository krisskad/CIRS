from rest_framework import serializers
from api.models import SiteConfig


class ExtractSerializer(serializers.Serializer):
    company_name = serializers.CharField()

    class Meta:
        fields = ['company_name']


class SiteConfigSerializer(serializers.ModelSerializer):
    """Serializer for Site Configuration"""
    class Meta:
        model = SiteConfig
        fields = "__all__"