from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class SiteConfig(models.Model):
    # Packages
    trial_limit = models.IntegerField(default=10)
    standard_limit = models.IntegerField(default=50)
    business_limit = models.IntegerField(default=100)
    # track updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def content_file_name(instance, filename):
    return '/'.join(['assets', str(instance.user.id), filename])


class Extraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # search keyword
    search_term = models.CharField(max_length=256, null=False)
    # company details
    company_detail = models.TextField(null=True)
    # Store Extracted Files
    amazon = models.FileField(upload_to=content_file_name, null=True) # BASE_DIR -> assets -> uuid
    linkedin = models.FileField(upload_to=content_file_name, null=True) # BASE_DIR -> assets -> uuid
    twitter = models.FileField(upload_to=content_file_name, null=True) # BASE_DIR -> assets -> uuid
    # track updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
