from service import Service
from django.db import models


class PackageLevel(models.Model):
    
    # Package level description
    level = models.CharField(max_length=100, default='')
    unit_descriptor = models.CharField(max_length=50)


class PackageLevelService(Service):
    def __init__(self):
        super().__init__(PackageLevel)
