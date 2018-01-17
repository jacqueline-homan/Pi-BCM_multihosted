import logging
import traceback

class audit_handler(logging.Handler):
    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        username = record.__dict__.get('user', None)
        #if not username:
        #    if current_user.is_authenticated():
        #        username = current_user.username
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)

        logger     = record.__dict__.get('name', '')
        level      = record.__dict__.get('levelname', '')
        msg        = record.__dict__.get('msg', '')
        ip_address = record.__dict__.get('ip_address', None)

        from services import logs_service
        logs_service.create( logger = logger,
                              level = level,
                              trace = trace,
                                msg = msg,
                           username = username,
                         ip_address = ip_address )
