from service import Service
from uam.models import Organisation
from prefixes.models import PrefixService
from user.models import User
from audit.models import Log

organisation_service = Service(Organisation)
prefix_service = PrefixService
users_service = Service(User)
logs_service = Service(Log)
