from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from django.core.files import File
from rest_framework import status
from pathlib import Path

from api.serializers import *
from api.models import *
from .scrapper.amazon import AmazonScrape
import requests


class SiteConfigViewSet(ViewSet):
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = SiteConfigSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        item = self.queryset.get(pk=pk)
        serializer = SiteConfigSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtractData(ViewSet):
    queryset = Extraction.objects.all()
    serializer_class = ExtractSerializer
    permission_classes = (AllowAny, IsAuthenticated)

    def list(self, request):
        queryset = self.queryset.filter(user=request.user.id).values()
        return Response(queryset)

    def post(self, request):
        company_name = request.data.get("company_name", None)
        uuid = str(request.user.id)

        # scrape amazon
        amazon = AmazonScrape(uuid=uuid)
        filepath = amazon.scrape(search_term=company_name)
        # local_file = open(filepath)
        # content_file = File(local_file)
        # print(filepath)
        # print(content_file)
        queryset = Extraction.objects.create(
            user=request.user,
            search_term=company_name,
            amazon=Path(filepath).name
        )
        print(queryset)
        # local_file.close()

        return Response({"d":"f"})
