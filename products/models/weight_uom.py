from django.db import models


class WeightUOM(models.Model):
    # weight unit of measure
    uom = models.CharField(max_length=20, default='')
    abbr = models.CharField(max_length=10, default='')
    code = models.CharField(max_length=10, default='')
