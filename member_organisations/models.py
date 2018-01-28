from django.db import models
from organizations.abstract import (AbstractOrganization,
                                    AbstractOrganizationUser,
                                    AbstractOrganizationOwner)

from BCM.models import Country


class MemberOrganisation(AbstractOrganization):
    """
    GS1 Member Organisation
    """
    country = models.OneToOneField(Country, related_name="member_organisation", primary_key=True,
                                   on_delete=models.CASCADE)


class MemberOrganisationUser(AbstractOrganizationUser):
    pass

class MemberOrganisationOwner(AbstractOrganizationOwner):
    pass
