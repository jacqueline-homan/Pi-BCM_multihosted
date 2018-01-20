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

    def _getValid(self, nums):
        """
        Redeclared here due to cyclic import
        """
        if not nums: return None
        cd1 = nums[-1]
        meat = nums[0:-1][::-1]  # cut cd away, reverse string, since x3 always applays from right (BC)
        odds = sum(map(lambda i: int(i) * 3, list(meat[0::2])))
        evns = sum(map(lambda i: int(i), list(meat[1::2])))
        cd2 = str(10 - ((odds + evns) % 10))[-1]  # 0 if 10 or reminder
        return nums[0:-1] + cd2

    def get_range(self):
        start = self._getValid('{0:0<13}'.format(self.prefix))
        end = self._getValid('{0:9<13}'.format(self.prefix))
        return start, end

    def get_capacity(self):
        return 10 ** (12 - len(self.prefix))

    def is_upc(self):
        return self.prefix.startswith("0")