import math
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

    def get_available_gtins(self, products, len_only=False):
        avail_gtins = []
        last_digits = int(math.log10(self.get_capacity()))
        if len(products) > 0:
            gtins = set([int(p.gtin[:-1][-last_digits:]) for p in products])
            avail = set(range(self.get_capacity()))
            try:
                if len_only:
                    _avail_gtins = avail.difference(gtins)
                else:
                    _avail_gtins = sorted(avail.difference(gtins))
            except:
                raise Exception(
                    "There are no available numbers left in this range. All numbers have now been allocated. To licence an additional company prefix please "
                    "go to the <a href='http://www.gs1ie.org/Members-Area'>Members Area</a> of the GS1 Ireland website.")
        else:
            _avail_gtins = set(range(self.get_capacity()))
        if len_only:
            return len(_avail_gtins)
        for gtin in _avail_gtins:
            f = '{0:0%d}' % (12 - len(self.prefix))
            avail_gtins.append("0" + self._getValid(self.prefix + f.format(gtin) + "0"))
        return avail_gtins

    def get_available_glns(self, locations, len_only=False):
        avail_glns = []
        last_digits = int(math.log10(self.get_capacity()))
        if len(locations) > 0:
            glns = set([int(p.gln[:-1][-last_digits:]) for p in locations])
            avail = set(range(self.get_capacity()))
            try:
                if len_only:
                    _avail_glns = avail.difference(glns)
                else:
                    _avail_glns = sorted(avail.difference(glns))
            except:
                raise Exception(
                    "There are no available numbers left in this range. All numbers have now been allocated. To licence an additional company prefix please "
                    "go to the <a href='http://www.gs1ie.org/Members-Area'>Members Area</a> of the GS1 Ireland website.")
        else:
            _avail_glns = set(range(self.get_capacity()))
        if len_only:
            return len(_avail_glns)
        for gln in _avail_glns:
            f = '{0:0%d}' % (12 - len(self.prefix))
            avail_glns.append("0" + self._getValid(self.prefix + f.format(gln) + "0"))
        return avail_glns
