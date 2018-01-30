from django.db import models
from django.contrib.auth.models import User as AuthUser
#from uam.models import Organisation
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from service import Service


class User(models.Model):
    db_name = 'user'

    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    is_authenticated = True
    active = models.BooleanField(default=True)
    customer_role = models.CharField(max_length=20,  default='')

    # Terms and conditions agreement
    agreed = models.BooleanField(default=False)
    agreed_date = models.DateTimeField(default=timezone.now)
    agreed_version = models.CharField(max_length=30, null=True, default='')

    login_count = models.IntegerField(null=True)

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

    # Show advanced tab?
    advanced_tab = db.Column(db.Boolean, default=False)
    # Enable leading digit?
    enable_leading = db.Column(db.Boolean, default=False)
    '''


@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, created, **kwargs):
    user = User.objects.filter(user=instance).first()
    if user:
        instance.user.save()
    else:
        user = User(user=instance)
        user.save()


class UsersService(Service):
    def __init__(self):
        super().__init__(User)

    def get_or_create(self, email, defaults={}):
        # get or create user
        auth_user, auth_user_created = AuthUser.objects.get_or_create(email=email, defaults={'username': email})

        # link user to the organisations
        member_organisation = defaults.get('member_organisation', None)
        if auth_user_created and member_organisation:
            member_organisation.add_user(auth_user)

        company_organisation = defaults.get('company_organisation', None)
        if auth_user_created and company_organisation:
            company_organisation.add_user(auth_user)

        return auth_user, auth_user_created

    def get_company_organisation(self, user):
        company_organisation = user.company_organisations_companyorganisation.first()
        return company_organisation

    def find(self, **kwargs):
        auth_user = AuthUser.objects.filter(email=kwargs['email']).first()
        #res = User.objects.filter(user=auth_user, customer_role=kwargs['customer_role'])
        #if res:
        return auth_user
