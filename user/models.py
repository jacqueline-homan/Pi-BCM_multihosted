from django.db import models
from service import Service
from uam.models import Organisation


class User(models.Model):
    db_name = 'users'

    email         = models.CharField(max_length=255, default='', unique=True)
    username      = models.CharField(max_length=50,  default='', unique=True)
    password      = models.CharField(max_length=255, default='')
    first_name    = models.CharField(max_length=30,  default='')
    last_name     = models.CharField(max_length=30,  default='')
    active        = models.BooleanField(default=True)

    organisation  = models.ForeignKey(Organisation, null=True, on_delete=models.PROTECT)
    customer_role = models.CharField(max_length=20,  default='')


    '''
    confirmed_at = models.DateTimeField()
    stripe_id    = models.CharField(max_length=255, nullable=True)
                               
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    barcodes = db.relationship("Barcode", back_populates="user",
                               cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="user",
                             cascade="all, delete-orphan")
    items = db.relationship("OrderedItem", back_populates="user",
                            cascade="all, delete-orphan")
    services = db.relationship("BCService", back_populates="user",
                               cascade="all, delete-orphan")

     new
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    organisation = db.relationship("Organisation", back_populates="users", cascade="all, delete-orphan",
                                   single_parent=True)

    customer_role = db.Column(
        db.Enum('regular', 'subscriber', 'partner', 'gs1ie', name='gs1ie_customer_role'))

    last_login = db.Column(db.DateTime, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=True,
                            default=datetime.utcnow())

    # added to enable traceable
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    # Terms and conditions agreement
    agreed = db.Column(db.Boolean, default=False)
    agreed_date = db.Column(db.DateTime, nullable=True)
    agreed_version = db.Column(db.String(30), default='')

    # Show advanced tab?
    advanced_tab = db.Column(db.Boolean, default=False)
    # Enable leading digit?
    enable_leading = db.Column(db.Boolean, default=False)
    '''


users_service = Service(User)
