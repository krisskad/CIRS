import pandas as pd
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.response import Response
# from django.core.files import File
from rest_framework import status
from pathlib import Path

from api.serializers import *
from api.models import *
from accounts.models import Packages
from accounts.serializers import PackageSerializer
from .scrapper.amazon import AmazonScrape
import requests
import numpy as np

class SiteConfigViewSet(ViewSet):
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = PackageSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        item = self.queryset.get(pk=pk)
        serializer = PackageSerializer(item, data=request.data)
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
        if request.user.coins < Packages.objects.get(package_name='trial').search_limit or request.user.is_admin:
            company_name = request.data.get("company_name", None)
            uuid = str(request.user.id)

            # scrape amazon
            amazon = AmazonScrape(uuid=uuid)
            filepath = amazon.scrape(search_term=company_name)

            # save data
            queryset = Extraction.objects.create(
                user=request.user,
                search_term=company_name,
                amazon=Path(filepath).name
            )

            print(queryset)

            # send scraped data
            amazon_df = pd.read_csv(filepath).replace(np.nan, None)
            context = {
                "amazon":amazon_df.to_dict(orient='records')
            }

            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Search limit exceeded"}, status=status.HTTP_401_UNAUTHORIZED)
