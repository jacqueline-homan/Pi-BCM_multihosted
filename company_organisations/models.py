from django.db import models
from organizations.abstract import (AbstractOrganization,
                                    AbstractOrganizationUser,
                                    AbstractOrganizationOwner)

from BCM.models import Country
from member_organisations.models import MemberOrganisation


class CompanyOrganisation(AbstractOrganization):
    """
    Company Organisation
    """
    member_organisation = models.ForeignKey(MemberOrganisation, on_delete=models.CASCADE, related_name="companies")

    uuid = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None, null=True)
    company = models.CharField(max_length=100, default='')

    street1 = models.CharField(max_length=100, default='')
    street2 = models.CharField(max_length=100, default='')

    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    zip = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='')
    gln = models.CharField(max_length=13, default='')
    vat = models.CharField(max_length=12, default='')

    credit_points_balance = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    # users = db.relationship('User', back_populates='organisation')
    # prefixes = db.relationship('Prefix', back_populates='organisation', cascade='all, delete-orphan')

    prefix_override = models.CharField(max_length=100,
                                       default='')  # to add additional prefixes overriding anything that DK sends

    def __str__(self):
        return "{} ({})".format(self.uuid, self.company)


class CompanyOrganisationUser(AbstractOrganizationUser):
    pass


class CompanyOrganisationOwner(AbstractOrganizationOwner):
    pass
