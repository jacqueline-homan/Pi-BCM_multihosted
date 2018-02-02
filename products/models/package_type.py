from django.db import models


class ServiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class PackageType(models.Model):
    # Package level description
    type = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=10, default='')
    image_path = models.CharField(max_length=70, default='')
    description = models.TextField(default='')
    ui_enabled = models.BooleanField(default=False)
    objects = models.Manager()
    service = ServiceManager()
