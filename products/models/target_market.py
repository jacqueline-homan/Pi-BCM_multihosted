from django.db import models


class TargetMarket(models.Model):
    code = models.CharField(max_length=10, db_index=True, unique=True, null=False)
    market = models.CharField(max_length=75, null=False)


