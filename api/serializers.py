from rest_framework import serializers

class ExtractSerializer(serializers.Serializer):
    company_name = serializers.CharField()

    class Meta:
        fields = ['company_name']
