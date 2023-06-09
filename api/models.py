from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class SiteConfig(models.Model):
    site = models.OneToOneField(Site)
    # Packages
    trial_limit = models.IntegerField(default=10)
    standard_limit = models.IntegerField(default=50)
    business_limit = models.IntegerField(default=100)
    # track updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def content_file_name(instance, filename):
    return '/'.join(['assets', instance.user.uuid, filename])


class Extraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # search keyword
    search_term = models.CharField(max_length=256, null=False)
    # Store Extracted Files
    amazon = models.FilePathField(default=content_file_name)
    linkedin = models.FilePathField(upload_to=content_file_name)
    twitter = models.FilePathField(upload_to=content_file_name)
    # track updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
