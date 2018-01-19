from django.db import models
from django.utils import timezone

from uam.models import Organisation


class Prefix(models.Model):
    class Meta:
        verbose_name_plural = "prefixes"

    db_name = 'prefixes'

    prefix = models.CharField(max_length=12, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_special = models.CharField(max_length=20, default='')
    # db.Enum('NULL', 'READ-ONLY', 'EACH-ONLY', 'PACK-ONLY', 'CASE-ONLY', 'PALLET-ONLY',
    #          name='prefix_special_status'), default='NULL')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    starting_from = models.CharField(max_length=13, null=True)
    starting_from_gln = models.CharField(max_length=13, null=True)

    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.PROTECT)

    description = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.prefix

    def __str__(self):
        return self.prefix

    def get_capacity(self):
        return 10 ** (12 - len(self.prefix))
