from service import Service
from uam.models import Organisation
from prefixes.models import Prefix
from user.models import User
from audit.models import Log

organisation_service = Service(Organisation)
prefix_service = Service(Prefix)
users_service = Service(User)
logs_service = Service(Log)
