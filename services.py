from service import Service
from uam.models import Organisation
from prefixes.models import Prefix
from user.models import User


organisation_service = Service(Organisation)
prefix_service = Service(Prefix)
users_service = Service(User)
