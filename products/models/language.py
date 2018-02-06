from django.db import models


class Language(models.Model):
    slug = models.CharField(max_length=5, db_index=True, unique=True, null=False)
    name = models.CharField(max_length=75, null=False)
