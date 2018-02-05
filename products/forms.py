from django import forms


# used in /products/add or /products/<id>/edit
class PackageLevelForm(forms.Form):
    package_level = forms.ChoiceField(widget=forms.RadioSelect)

    def set_package_levels(self, rows):
        self.fields['package_level'].choices = [(str(row.id), row.level) for row in rows]


# used in /products/add/<id>/basic or /products/<id>/edit/basic
class PackageTypeForm(forms.Form):
    package_type = forms.ChoiceField(widget=forms.Select, label='')
    bar_placement = forms.HiddenInput()

    def set_package_types(self, rows):
        self.fields['package_type'].choices = [(str(row.id), row.type) for row in rows]


class ProductDetailForm(forms.Form):
    gtin = forms.HiddenInput()
    bar_placement = forms.HiddenInput()
    package_level_id = forms.HiddenInput()
    package_type_id = forms.HiddenInput()

    # Company Name
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    # Label Description
    label_description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) #'Label Description', [Required("Label Description: This field is required.")])

    # Brand
    brand = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'brand'}))     # 'Brand', [Required("Brand: This field is required.")])

    # Sub brand
    sub_brand = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'sub_brand'}))

    # Product Type/Functional Name
    functional_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'functional_name'}))   # TextField('Product Type/Functional Name:', [Required("Product Type/Functional Name: This field is required.")])

    # Sub brand
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'variant'}))

    # Product/Trade Item Description
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'description'})) # 'Product/Trade Item Description', [Required("Product/Trade Item Description: This field is required.")])

    # Global Product Classification
    category = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) # [Required("GPC: This field is required."), Regexp('^[0-9]{8}$', message="Should be 8 digits."), check_category])

    # Company/Internal Product Code or SKU
    sku = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    # Country Of Origin
    country_of_origin = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'country_of_origin'}))

    # Target Market
    target_market = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'target_market'}))

    # Language
    language = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'language'}))

    # GLN of Information provider
    gln_of_information_provider = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'gln_of_information_provider'})) #'', [Regexp('^[0-9]{13}$', message="Should be 13 digits."), check_gln])

    # The item is a Base Unit
    is_bunit = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'is_bunit'}))

    is_cunit = forms.BooleanField()     # The item is a Consumer Unit
    is_dunit = forms.BooleanField()     # The item is a Dispatch Unit
    is_vunit = forms.BooleanField()     # The item is a Variable Weight Product
    is_iunit = forms.BooleanField()     # The item is an Invoice Unit
    is_ounit = forms.BooleanField()     # The item is an Orderable Unit

    # Gross Weight
    gross_weight = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'gross_weight'}))
    gross_weight_uom = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'gross_weight_uom'}))

    # Net Weight
    net_weight = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'net_weight'}))
    net_weight_uom = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'net_weight_uom'}))

    # Depth
    depth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'depth'}))
    depth_uom = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'depth_uom'}))

    # Width
    width = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'width'}))
    width_uom = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'width_uom'}))

    # Height
    height = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'height'}))
    height_uom = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'height_uom'}))

    # External image URL (if hosted)
    website_url = forms.URLField(widget=forms.TextInput(attrs={'class':'form-control'}))   # URLField('', [Optional(), URL(require_tld=True, message=u'Invalid URL.')])

    def is_valid(self):
        '''
        Vaidation function, we are not using djando validation
        :return:
        '''

        # form_errors = check_values(template_name, form, **context)
        # if form_errors is not None:
        #     return form_errors
        # Clean empty values from formfields

        return True
