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
from .scrapper.main import main

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
        if request.user.is_superuser:
            queryset = self.queryset.values()
        else:
            queryset = self.queryset.filter(user=request.user.id).values()
        return Response(queryset)

    def post(self, request):
        if request.user.coins < Packages.objects.get(package_name='trial').search_limit or request.user.is_superuser:
            company_name = request.data.get("company_name", None)
            uuid = str(request.user.id)

            # save data
            extract_ins = Extraction(user=request.user, search_term=company_name)

            result = main(search_term=company_name, uuid=uuid)

            # Update the extract_ins object with the scraped data
            extract_ins.company_detail = result["company_detail"]
            extract_ins.amazon = str(result["amazon"]).split("/media/")[-1]
            extract_ins.linkedin = result["linkedin"]

            # save
            extract_ins.save()

            # send scraped data
            # result["amazon_products"] = pd.read_csv(result["amazon"]).replace(np.nan, None).to_dict(orient='records')
            context = {
                "company_detail":extract_ins.company_detail,
                "linkedin_data":extract_ins.linkedin,
                "amazon":str(request.build_absolute_uri(extract_ins.amazon.url))
            }

            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Search limit exceeded"}, status=status.HTTP_401_UNAUTHORIZED)
