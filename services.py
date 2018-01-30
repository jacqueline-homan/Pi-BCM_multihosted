from service import Service
from prefixes.models import PrefixService, Prefix
from users.models import UsersService
from audit.models import Log
from products.models import Product

prefix_service = PrefixService()
users_service = UsersService()
logs_service = Service(Log)
product_service = Service(Product)
