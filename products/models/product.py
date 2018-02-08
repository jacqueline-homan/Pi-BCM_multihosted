from django.db import models
from django.contrib.auth.models import User
from company_organisations.models import CompanyOrganisation
from member_organisations.models import MemberOrganisation
from .target_market import TargetMarket
from .country_of_origin import CountryOfOrigin
from .language import Language
from .dimension_uom import DimensionUOM
from .weight_uom import WeightUOM


class ServiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, **kwargs):
        fields_data = {}
        for field in Product._meta.get_fields():
            if field.name == 'depth_uom':
                continue
            if field.name == 'width_uom':
                continue
            if field.name == 'height_uom':
                continue
            if field.name == 'gross_weight_uom':
                continue
            if field.name == 'net_weight_uom':
                continue
            if field.name == 'country_of_origin':
                continue
            if field.name == 'target_market':
                continue
            if field.name == 'language':
                continue
            if field.name in kwargs.keys():
                fields_data[field.name] = kwargs[field.name]

        product = Product(**fields_data)
        product.save()
        return product


class Product(models.Model):
    # product owner info
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    company_organisation = models.ForeignKey(CompanyOrganisation, null=True, on_delete=models.PROTECT)
    member_organisation = models.ForeignKey(MemberOrganisation, null=True, on_delete=models.PROTECT)

    # Product info
    gtin = models.CharField(max_length=14, default='', blank=True, db_index=True)
    gs1_company_prefix = models.CharField(max_length=75, default='', blank=True, db_index=True)
    gln_of_information_provider = models.CharField(max_length=75, null=True)
    category = models.CharField(max_length=75, null=True)
    # attributes = models.CharField(max_length=500)
    # label_description = models.CharField(max_length=500)

    # barcodes = models.ForeignKey('Barcode')
    # package_level = models.ForeignKey('PackageLevel')
    # package_type = models.ForeignKey('PackageType', null=True)

    # Used for books with this mapping:
    description = models.CharField(max_length=200, null=True)  # functiona_name
    sku = models.CharField(max_length=75, null=True)
    brand = models.CharField(max_length=75, null=True)  # publisher
    sub_brand = models.CharField(max_length=75, null=True)
    functional_name = models.CharField(max_length=75, null=True)  # title
    variant = models.CharField(max_length=75, null=True)  # info

    # use product.add_image(request.files['img']) method to save image
    # image = models.CharField()

    # Dimensions
    depth = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    depth_uom = models.ForeignKey(DimensionUOM, null=True, on_delete=models.CASCADE, related_name='products_depth')
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    width_uom = models.ForeignKey(DimensionUOM, null=True, on_delete=models.CASCADE, related_name='products_width')
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height_uom = models.ForeignKey(DimensionUOM, null=True, on_delete=models.CASCADE, related_name='products_height')

    # Qualified  values
    # net_content = models.CharField(max_length=10)
    # net_content_uom = models.ForeignKey("NetContentUOM")
    gross_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    gross_weight_uom = models.ForeignKey(WeightUOM, null=True, on_delete=models.CASCADE, related_name='products_grossweight')
    net_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    net_weight_uom = models.ForeignKey(WeightUOM, null=True, on_delete=models.CASCADE, related_name='products_netweight')

    # Company details
    company = models.CharField(max_length=100, null=True)
    # contact = models.CharField(max_length=50)
    # address = models.CharField(max_length=200)
    # company_phone = models.CharField(max_length=20)
    # company_email = models.CharField(max_length=75)

    # Auto fill fields - TODO
    # bar_type = db.Column(
    #    db.Enum('NULL', 'UPCA', 'EAN13', 'RSS14', 'ISBN13', 'ITF14', name='gs1ie_bc_kind'), default='EAN13',
    #    nullable=False)

    # bar_placement = models.CharField(50, default='/static/site/img/empty.gif')
    # avail_barcode_height = models.CharField(75)
    # avail_barcode_width = models.CharField(75)

    country_of_origin = models.ForeignKey(CountryOfOrigin, null=True, on_delete=models.CASCADE )
    point_of_sale = models.CharField(max_length=75, null=True)
    website_url = models.CharField(max_length=256, null=True)
    # enquiries = models.CharField(null=True)

    is_bunit = models.BooleanField(default=False)
    is_cunit = models.BooleanField(default=False)
    is_dunit = models.BooleanField(default=False)
    is_vunit = models.BooleanField(default=False)
    is_iunit = models.BooleanField(default=False)
    is_ounit = models.BooleanField(default=False)
    # is_temp = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # is_public = models.BooleanField(default=False)

    # pub_date = models.DateTimeField(null=True)  # AQ
    # eff_date = models.DateTimeField(null=True)  # AR
    # created = db.Column(db.DateTime, default=datetime.datetime.now)
    # updated = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    #  GDSN ADDITIONS
    name_of_information_provider = models.CharField(max_length=100, null=True)
    target_market = models.ForeignKey(TargetMarket, null=True, on_delete=models.CASCADE)
    # start_availability = db.Column(db.DateTime)
    # returnable = db.Column(db.Boolean, default=False)
    # end_availability = db.Column(db.DateTime)
    # last_change = db.Column(db.DateTime)
    # brand_owner_gln = db.Column(db.String(13))
    # brand_owner_name = db.Column(db.String(100))
    # discontinued_date = db.Column(db.DateTime)

    # GEPIR ADDITIONS
    language = models.ForeignKey(Language, null=True, on_delete=models.CASCADE)
    # role_of_information_provider_id = db.Column(db.Integer, db.ForeignKey("iprole.id"))
    # role_of_information_provider = db.relationship("IPRole", foreign_keys=role_of_information_provider_id)
    # additional_identification_of_ip = db.Column(db.String(100))
    # manufacturer_gln = db.Column(db.String(13))
    # manufacturer_name = db.Column(db.String(75))
    # manufacturer_role_id = db.Column(db.Integer, db.ForeignKey("iprole.id"))
    # manufacturer_role = db.relationship("IPRole", foreign_keys=manufacturer_role_id)
    # manufacturer_additional_identification = db.Column(db.String(100))
    # category_definition = db.Column(db.String(200))
    # category_name = db.Column(db.String(75))
    # additional_classification_code = db.Column(db.String(75))
    # descriptive_size = db.Column(db.String(75))
    # size_code = db.Column(db.String(25))
    # is_price_on_pack = db.Column(db.Boolean, default=False)

    # GS1 CLoud additions
    gs1_cloud_state = models.CharField(max_length=75, null=True)
    # gs1_cloud_state = db.Column(
    #    db.Enum(*GS1_CLOUD_STATES_ENUM.keys(), name='gs1_cloud_state'), default='INACTIVE', nullable=False)
    # gs1_cloud_last_rc = db.Column(db.Enum(*GS1_CLOUD_RC_ENUM.keys(), name='gs1_cloud_rc_enum'), nullable=True)
    # gs1_cloud_last_update = db.Column(db.DateTime())
    # gs1_cloud_last_update_ref = db.Column(db.String(20), nullable=True, index=True)

    # PLACEHOLDER FOR UI ( to be able to favorite an item )
    # mark = db.Column(db.Integer, nullable=True, default=0)

    objects = models.Manager()
    service = ServiceManager()

