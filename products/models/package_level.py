from service import Service
from django.db import models


class ServiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class PackageLevel(models.Model):
    # Package level description
    level = models.CharField(max_length=100, default='')
    unit_descriptor = models.CharField(max_length=50)
    objects = models.Manager()
    service = ServiceManager()


class PackageLevelService(Service):
    def __init__(self):
        super().__init__(PackageLevel)

