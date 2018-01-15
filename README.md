# BCM_multihosted

Setup instruction:

1. ./manage.py migrate
2. ./manage.py loaddata default.json
3. ./manage.py createsuperuser

This gives a some default values for languages and simple demonstration of template transaltion. After unathorized user select country, django. read default languages for it (or use random choice for demonstration) and next page with language select will be translated.
