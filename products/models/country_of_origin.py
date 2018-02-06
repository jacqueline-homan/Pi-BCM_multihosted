from django.db import models


class CountryOfOrigin(models.Model):
    code = models.CharField(max_length=10, db_index=True, unique=True, null=False)
    name = models.CharField(max_length=75, null=False)
