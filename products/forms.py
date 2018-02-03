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
    gln_of_information_provider = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) #'', [Regexp('^[0-9]{13}$', message="Should be 13 digits."), check_gln])
    is_bunit = forms.BooleanField()
