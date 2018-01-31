from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from services import prefix_service, package_level_service
from core import flash
from .apps import subproducts_reset
from .models.package_level import PackageLevel


def add_product(request):
    """
    GET/POST for adding a new base or case product
    :return:
    """
    prefix = None
    subproducts_reset(request.session)  # remove subproducst from session if any
    if request.POST.get('prefix'):
        prefix = prefix_service.find_item(prefix=request.args.get('prefix'))
        if prefix and not prefix.is_active:
            prefix_service.make_active(prefix)
        if request.session.get('new_product', None):
            del request.session['new_product']
    else:
        prefix = prefix_service.find_item(is_active=True)
    if not prefix:
        flash('You must have an active prefix set to enter new product. Please choose one', 'danger')
        return redirect(reverse('prefixes:prefixes_list'))
    if not prefix.starting_from:
        flash('You must have a starting number set to enter new product. Please set one', 'danger')
        return redirect(reverse('prefixes:prefixes_list'))
    if prefix.is_special == 'READ-ONLY':
        flash('You can not add a new product in this range. It\'s a suspended read-only range', 'danger')
        return redirect(reverse('products:products_list'))

    if prefix.is_special != 'NULL':
        #package_rows = services.package_level_service.find(
        #    id=models.PACKAGE_LEVEL_SPECIAL_ENUM[prefix.is_special]).all()
        package_rows = None
    else:
        package_rows = package_level_service.all()

    '''
    title = "New Product"
    if request.args.get('express'):
        title = "Express Allocation"
    if request.method == 'POST':
        form = forms.PackageLevelForm(request.form)
        form.set_package_levels(package_rows)
        if form.validate():
            if not session.get('new_product', None):
                session['new_product'] = {'gtin': str(prefix.starting_from), 'package_level': form.package_level.data}
            elif session.get('new_product')['gtin'] != str(prefix.starting_from):
                session['new_product'] = {'gtin': str(prefix.starting_from), 'package_level': form.package_level.data}
            else:
                session['new_product']['package_level'] = form.package_level.data
            if request.args.get('express'):
                session['new_product'].update({'express': True})
            elif 'express' in session['new_product']:
                del session['new_product']['express']
            return redirect(url_for('products.add_product_package_type'))
            # if session['new_product']['package_level'] == str(models.BASE_PACKAGE_LEVEL):
            #    if session['new_product'].get('express'):
            #        return redirect(url_for('products.add_product_express'))
            #    else:
            #        return redirect(url_for('products.add_product_package_type'))
            # else:
            #    return redirect(url_for('products.add_product_select_sub'))
        else:
            flash('You must choose a level to proceed', 'danger')
    else:
        form = forms.PackageLevelForm()
        form.set_package_levels(package_rows)
        if session.get('new_product', None) and session.get('new_product')['gtin'] == str(prefix.starting_from):
            form.package_level.data = session.get('new_product')['package_level']
    '''

    context = { 'title': 'New Product',
               'prefix': prefix }

    return render(request, 'products/package_level_form.html', context)


def products_list(request):
    return HttpResponse('products.products_list page')
