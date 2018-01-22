from django.db import models
import random
# from organizations.models import
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=2)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    def get_default_language(self):
    	default_lang = LanguageByCountry.objects.filter(country=self, default=True).first()
    	if default_lang:
    		return default_lang
    	else:
    		return random.choice(LanguageByCountry.objects.filter(country=self))


class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=2)

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)


class LanguageByCountry(models.Model):
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Languages by countries"

    def __str__(self):
        return "{}_{}".format(self.country.slug, self.language.slug)

    def save(self):
        if self.default:
            queryset = LanguageByCountry.objects.filter(
                country=self.country, default=True).exclude(id=self.id).all()
            for record in queryset:
                record.default = False
                record.save()
        super(LanguageByCountry, self).save()
    
class Product(db.Model):
    class Meta:

        db_name = "products"
        unique_together = (('owner_id', 'gtin'), )

        indexes = [
            models.Index(fields=['gtin']),
            models.Index(fields=['gs1_company_prefix'])
        ]

   

    # product owner info
    owner = models.ForeignKey('Owner')
    

    # organisation
    organisation = models.ForeignKey(db.Integer, db.ForeignKey('Organisation')
    

    # Product info
    gtin = models.CharField(max_length=14)
    gs1_company_prefix = models.CharField(max_length=75)
    gln_of_information_provider = models.CharField(max_length=75)
    
    category = models.CharField(max_length=75)

    attributes = models.CharField(max_length=500)
    
    # target_market = CountryField(blank = True)
    labelDescription = models.CharField(max_length=500)
    

    barcodes = models.ForeignKey('Barcode')
    

    package_level = models.ForeignKey('PackageLevel')

    package_type = models.ForeignKey('PackageType', null=True)

    # Used for books with this mapping:
    description = models.CharField(max_length=200)  # functiona_name
    sku = models.CharField(max_length=75, null=True)
    brand = models.CharField(max_length=75)  # publisher
    sub_brand = models.CharField(max_length=75, null=True)
    functional_name = models.CharField(max_length=75)  # title
    variant = models.CharField(max_length=75, nullable=True)  # info

    # use product.add_image(request.files['img']) method to save image
    image = models.CharField()

    # Dimensions
    depth_uom = models.ForeignKey('DimensionUOM')

    depth = models.DecimalField(precision=8, scale=2)

    width_uom = models.ForeignKey("DimensionUOM")
    width = models.DecimalField(max_digits=8, decimal_places=2)

    height_uom = models.ForeignKey("DimensionUOM")
    height = models.DecimalField(max_digits=8, decimal_places=2)

    # Qualified  values
    net_content = models.CharField(max_length=10)
    net_content_uom = models.ForeignKey("NetContentUOM")

    gross_weight = models.DecimalField(max_digits=8, decimal_places=2)
    gross_weight_uom = models.ForeignKey("WeightUOM")

    net_weight = models.DecimalField(max_digits=8, decimal_places=2)
    net_weight_uom = models.ForeignKey("WeightUOM")

    point_of_sale = models.CharField(max_length=75)

    # Company details
    company = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    company_phone = models.CharField(max_length=20)
    company_email = models.CharField(max_length=75)

    # Auto fill fields
    bar_type = db.Column(
        db.Enum('NULL', 'UPCA', 'EAN13', 'RSS14', 'ISBN13', 'ITF14', name='gs1ie_bc_kind'), default='EAN13',
        nullable=False)

    bar_placement = models.CharField(50, default='/static/site/img/empty.gif')
    avail_barcode_height = models.CharField(75)
    avail_barcode_width = models.CharField(75)

    country_of_origin = models.ForeignKey('CountryOfOrigin')
    

    website_url = models.CharField(null=True)
    enquiries = models.CharField(null=True)

    is_bunit = models.BooleanField(default=False)
    is_cunit = models.BooleanField(default=False)
    is_dunit = db.Column(db.Boolean, default=False)
    is_vunit = db.Column(db.Boolean, default=False)
    is_iunit = db.Column(db.Boolean, default=False)
    is_ounit = db.Column(db.Boolean, default=False)
    is_temp = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)

    pub_date = db.Column(db.DateTime)  # AQ
    eff_date = db.Column(db.DateTime)  # AR

    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    #  GDSN ADDITIONS
    name_of_information_provider = models.CharField(100))
    target_market_id = db.Column(db.Integer, db.ForeignKey("target_market.id"), nullable=False)
    target_market = db.relationship("TargetMarket", backref="products")
    start_availability = db.Column(db.DateTime)
    returnable = db.Column(db.Boolean, default=False)
    end_availability = db.Column(db.DateTime)
    last_change = db.Column(db.DateTime)
    brand_owner_gln = models.CharField(13))
    brand_owner_name = models.CharField(100))
    discontinued_date = db.Column(db.DateTime)

    # GEPIR ADDITIONS
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)
    language = db.relationship("Language", backref="products")
    role_of_information_provider_id = db.Column(db.Integer, db.ForeignKey("iprole.id"))
    role_of_information_provider = db.relationship("IPRole", foreign_keys=role_of_information_provider_id)
    additional_identification_of_ip = models.CharField(100))
    manufacturer_gln = models.CharField(13))
    manufacturer_name = models.CharField(75))
    manufacturer_role_id = db.Column(db.Integer, db.ForeignKey("iprole.id"))
    manufacturer_role = db.relationship("IPRole", foreign_keys=manufacturer_role_id)
    manufacturer_additional_identification = models.CharField(100))
    category_definition = models.CharField(200))
    category_name = models.CharField(75))
    additional_classification_code = models.CharField(75))
    descriptive_size = models.CharField(75))
    size_code = models.CharField(25))
    is_price_on_pack = db.Column(db.Boolean, default=False)

    # GS1 CLoud additions
    gs1_cloud_state = db.Column(
        db.Enum(*GS1_CLOUD_STATES_ENUM.keys(), name='gs1_cloud_state'), default='INACTIVE', nullable=False)
    gs1_cloud_last_rc = db.Column(db.Enum(*GS1_CLOUD_RC_ENUM.keys(), name='gs1_cloud_rc_enum'), nullable=True)
    gs1_cloud_last_update = db.Column(db.DateTime())
    gs1_cloud_last_update_ref = models.CharField(36), nullable=True, index=True)

    # PLACEHOLDER FOR UI ( to be able to favorite an item )
    mark = db.Column(db.Integer, nullable=True, default=0)

    def __unicode__(self):
        return '%s | %s | %s' % (self.gtin, self.description, self.brand)


    def get_absolute_url(self):
        return '/products/%d/fulledit' % self.id

    def add_image(self, file):
        """
        Saves image in PRODUCT_IMAGES and save relative file path in
        self.image
        """
        assert str(self.owner), "owner must be set before saving product image"
        ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        filename = file.filename
        if file and '.' in filename and \
                        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:

            filename = secure_filename(filename)
            if not os.path.exists(os.path.join(current_app.config['PRODUCT_IMAGES'], str(self.owner_id))):
                os.mkdir(os.path.join(current_app.config['PRODUCT_IMAGES'], str(self.owner_id)))
            relative_filepath = os.path.join(str(self.owner_id), filename)
            destination = os.path.join(current_app.config['PRODUCT_IMAGES'],
                                       relative_filepath)
            file.save(destination)
            self.image = current_app.config['GS1_INSTANCE_DOMAIN'] + '/static/product_images/' + relative_filepath
            self.website_url = self.image
        else:
            raise Exception("Supported file extensions are %r: (%r given)" %
                            (ALLOWED_IMAGE_EXTENSIONS, filename))

    def number_of_products(self):
        assert self.package_level_id != BASE_PACKAGE_LEVEL
        subs = self.associated_sub_products.all()
        for sub in subs:
            if sub.sub_product.package_level_id == BASE_PACKAGE_LEVEL or sub.sub_product.number_of_products() is None:
                return sub.quantity
            else:
                return sub.quantity * sub.sub_product.number_of_products()
        return None

    def get_leading(self):
        return normalize('EAN13', self.gs1_company_prefix)

    def to_gdsn(self):

        def internal_bar_type_to_repr(bar_type):
            for key, value in BARCODE_TYPES.items():
                if value == bar_type:
                    return key
            logging.error('could not map barcode_type for %s' % self.gtin)
            return 'EAN_13'

        data = {
            "Label_Description": self.labelDescription,
            "Trade_Item_GTIN": self.gtin,
            "Information_Provider_GLN": self.gln_of_information_provider or self.get_leading(),
            "Information_Provider_Name": current_app.config.get('GS1_GEPIR_EXPORT_NAME', ''),
            "Target_Market": self.target_market.code if self.target_market else '372',
            "Base_Unit_Indicator": self.is_bunit,
            "Consumer_Unit_Indicator": self.is_cunit,
            "Variable_Weight_Trade_Item": self.is_vunit,
            "Ordering_Unit_Indicator": self.is_ounit,
            "Dispatch_Unit_Indicator": self.is_dunit,
            "Invoice_Unit_Indicator": self.is_iunit,
            "Start_Availability_Date_Time": self.start_availability,
            "Classification_Category_Code": str(self.category) if self.category else None,
            "Trade_Item_Unit_Descriptor": self.package_level.unit_descriptor if self.package_level else None,
            "Functional_Name": self.functional_name,
            "Brand_Name": self.brand,
            "Packaging_Marked_Returnable": self.returnable,
            "Height": self.height,
            "Height_UOM": self.height_uom.code if self.height_uom else None,
            "Width": self.width,
            "Width_UOM": self.width_uom.code if self.width_uom else None,
            "Depth": self.depth,
            "Depth_UOM": self.depth_uom.code if self.depth_uom else None,
            "Gross_Weight": self.gross_weight,
            "Gross_Weight_UOM": self.gross_weight_uom.code if self.gross_weight_uom else None,
            "End_Availability_Date_Time": self.end_availability,
            "Sub_Brand": self.sub_brand,
            "Brand_Owner_GLN": self.brand_owner_gln,
            "Brand_Owner_Name": self.brand_owner_name,
            "Product_Description": self.description,
            "Variant_Description": self.variant,
            "Packaging_Type_Code": self.package_type.code if self.package_type else None,
            "Trade_Item_Last_Change_Date": self.updated,
            "Discontinued_Date": self.discontinued_date,
            "Trade_Item_Country_Of_Origin": self.country_of_origin.code if self.country_of_origin else None,
            "Manufacturer_GLN": self.manufacturer_gln,
            "Manufacturer_Name": self.manufacturer_name,
            "Is_Price_On_Pack": self.is_price_on_pack,
            "Barcode_Type": internal_bar_type_to_repr(self.bar_type),
            "Additional_Trade_Item_Identification_Type": "SUPPLIER_ASSIGNED",
            "Additional_Trade_Item_Identification_Value": self.sku,
            # "Type_Of_Information": "WEBSITE",
            "Uniform_Resource_Identifier": self.website_url,
            "Trade_Item_Status": "ADD",
            "GS1CloudStatus": self.gs1_cloud_state,
            "Use_Language_Code_List": self.language.code if self.language else 'en',
            "Company_Name": self.company if self.company else self.organisation.company
        }
        if data['Trade_Item_Unit_Descriptor'] != 'BASE_UNIT_OR_EACH':
            data.update(
                {
                    "GTIN_Of_Next_Lower_Item": self.gtin_of_next_lower_item,
                    "Amount_Of_Next_Lower_Level_Items": self.total_quantity_of_next,
                    "Quantity_Of_Children": self.quantity_of_children,
                    "Total_Quantity_Of_Next_Lower_Level_Trade_Item": self.total_quantity_of_next
                }
            )
        else:
            data.update(
                {
                    "Net_Content": self.net_content,
                    "Net_Content_UOM": self.net_content_uom.code if self.net_content_uom else None,
                    "Net_Weight": self.net_weight,
                    "Net_Weight_UOM": self.net_weight_uom.code if self.net_weight_uom else None
                }
            )

        # if image url is present, we qualify it as PRODUCT_IMAGE in the export
        if self.website_url:
            data.update(
                {
                    "Type_Of_Information": "PRODUCT_IMAGE"
                }
            )

        # Dates
        current_ts = datetime.datetime.now()
        if not self.pub_date:
            data.update({"Publication_Date": current_ts, })
        else:
            data.update({"Publication_Date": self.pub_date})
        if not self.eff_date:
            data.update({"Effective_Date": current_ts})
        else:
            data.update({"Effective_Date": self.pub_date})
        if not self.start_availability:
            data.update({"Start_Availability_Date_Time": current_ts})
        else:
            data.update({"Start_Availability_Date_Time": self.start_availability})

        # pprint.pprint(data,indent=2)

        return data

    def to_gepir(self):
        data = {
            "Trade_Item_GTIN": self.gtin,
            "Item_Data_Language": "en",
            "Information_Provider_GLN": current_app.config.get('GS1_GEPIR_EXPORT_GLN', ''),
            "Information_Provider_Name": current_app.config.get('GS1_GEPIR_EXPORT_NAME', ''),
            "Product_Description": self.description,
            "Trade_Item_Unit_Descriptor": self.package_level.unit_descriptor if self.package_level else None,
            "Brand_Name": self.brand,
            "Net_Content": self.net_content,
            "Net_Content_UOM": self.net_content_uom.code if self.net_content_uom else None,
            "Trade_Item_Last_Change_Date": self.updated,
            "IPparty_Role": "INFORMATION_PROVIDER",
            "IPadditionalPartyIdentification": self.additional_identification_of_ip,
            "Manufacturer_GLN": self.manufacturer_gln,
            "Manufacturer_Name": self.manufacturer_name,
            "ManufacturerpartyRole": self.manufacturer_role.code if self.manufacturer_role else None,
            "ManufactureradditionalPartyIdentification": self.manufacturer_additional_identification,
            "Classification_Category_Code": self.category,
            "gpcCategoryDefinition": self.category_definition,
            "gpcCategoryName": self.category_name,
            "additionalTradeItemClassificationSystemCode": self.additional_classification_code,
            "descriptiveSize": self.descriptive_size,
            "sizeCode": self.size_code,
            "Uniform_Resource_Identifier": self.website_url,
        }
        if data['Trade_Item_Unit_Descriptor'] != 'BASE_UNIT_OR_EACH':
            data.update(
                {
                    "Quantity_Of_Children": self.quantity_of_children,
                    "Total_Quantity_Of_Next_Lower_Level_Trade_Item": self.total_quantity_of_next
                }
            )
        if data['Uniform_Resource_Identifier']:
            data.update(
                {
                    "fileFormatCode": 'HTML',
                }
            )

        if data.get("Manufacturer_GLN") and data.get("Manufacturer_Name"):
            data.update(
                {
                    "ManufacturerpartyRole": 'MANUFACTURER_OF_GOODS',
                }
            )

        return data

    @property
    def quantity_of_children(self):
        subs = self.associated_sub_products.all()
        return str(len(subs)) if subs else '0'

    @property
    def total_quantity_of_next(self):
        subs = self.associated_sub_products.all()
        totals = []
        for sub in subs:
            totals.append(str(sub.quantity))
        return ','.join(totals)

    @property
    def gtin_of_next_lower_item(self):
        subs = self.associated_sub_products.all()
        gtins = []
        for sub in subs:
            gtins.append(sub.sub_product.gtin)
        return ','.join(gtins)

    @property
    def get_is_bunit(self):
        if self.package_level_id == BASE_PACKAGE_LEVEL:
            return True
        return False

    @property
    def completeness(self):

        # print self

        cnt_available = 0
        cnt_present = 0

        comp_fields = [
            'category',
            'description',
            'sku',
            'brand',
            'sub_brand',
            'functional_name',
            'variant',

            'image',
            'depth',
            'height',
            'width',
            'gross_weight',

            'country_of_origin_id',
            'website_url',
        ]

        if self.package_level_id == BASE_PACKAGE_LEVEL:
            comp_fields.extend(['net_weight', 'net_content'])

        for comp_field in comp_fields:
            if self.__getattribute__(comp_field):
                cnt_present += 1
            cnt_available += 1
            # print comp_field, self.__getattribute__(comp_field)

        # print cnt_present, cnt_available

        unit_field_found = False
        cnt_available += 1
        for comp_field in 'is_cunit', 'is_dunit', 'is_vunit', 'is_iunit', 'is_ounit':
            if not unit_field_found:
                if self.__getattribute__(comp_field):
                    unit_field_found = True
        if unit_field_found:
            cnt_present += 1
        # print cnt_present, cnt_available
        return float(cnt_present) / float(cnt_available) * 100

