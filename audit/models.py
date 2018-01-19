from django.db import models
from django.utils import timezone


class Log(models.Model):
    db_name = 'log'

    logger     = models.CharField(max_length=50, null=True)  # the name of the logger. (e.g. myapp.views)
    level      = models.CharField(max_length=10, null=True)  # info, debug, or error?
    trace      = models.TextField(null=True)  # the full traceback printout
    msg        = models.TextField(null=True)  # any custom log you may have included
    ip_address = models.CharField(max_length=15, null=True)  # ip address
    username   = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # the current timestamp
