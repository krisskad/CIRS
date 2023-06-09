from django.shortcuts import render
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import *
from .scrapper.amazon import AmazonScrape
import requests


class AdminConfig(ViewSet):
    serializer_class = ExtractSerializer
    permission_classes = (IsAdminUser,)
    # permission_classes = (IsAuthenticated,)

    def list(self, request):

        queryset = {
            "USE CASE": "Configure the site settings and params",
            "TIP": "Params will be use to scrape the data and set the user limits",

        }
        return Response(queryset)

    def post(self, request):
        company_name = request.data.get("company_name", None)

        queryset = {
            "USE CASE": company_name,
            "TIP": "Choose check box to get that data in response",

        }
        return Response(queryset)


class ExtractData(ViewSet):
    serializer_class = ExtractSerializer
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        user = request.user.username
        queryset = {
            "user": user,

        }
        return Response(queryset)

    def post(self, request):
        company_name = request.data.get("company_name", None)

        queryset = {
            "USE CASE": company_name,
            "TIP": "Choose check box to get that data in response",

        }
        return Response(queryset)
