from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from services import prefix_service, package_level_service
from core import flash, flash_get_messages
from .apps import subproducts_reset
from .forms import PackageLevelForm
from .models.package_level import PackageLevel


def add_product(request):
    """
    GET/POST for adding a new base or case product
    :return:
    """
    subproducts_reset(request.session)  # remove subproducst from session if any
    prefix = request.POST.get('prefix', None)
    if prefix is None:
        prefix = request.GET.get('prefix', None)
    if prefix:
        prefix = prefix_service.find_item(prefix=prefix)
        if prefix and not prefix.is_active:
            prefix_service.make_active(prefix)
        if request.session.get('new_product', None):
            del request.session['new_product']
    else:
        prefix = prefix_service.find_item(is_active=True)
    if not prefix:
        flash(request, 'You must have an active prefix set to enter new product. Please choose one', 'danger')
        return redirect(reverse('prefixes:prefixes_list'))
    if not prefix.starting_from:
        flash(request, 'You must have a starting number set to enter new product. Please set one', 'danger')
        return redirect(reverse('prefixes:prefixes_list'))
    if prefix.is_special == 'READ-ONLY':
        flash(request, 'You can not add a new product in this range. It\'s a suspended read-only range', 'danger')
        return redirect(reverse('products:products_list'))

    #if prefix.is_special != 'NULL':
    #    package_rows = services.package_level_service.find(
    #        id=models.PACKAGE_LEVEL_SPECIAL_ENUM[prefix.is_special]).all()
    #else:
    #    package_rows = package_level_service.all()
    package_rows = PackageLevel.service.all()

    express = True if request.POST.get('express') or request.GET.get('express') else False

    title = 'New Product'
    if express:
        title = 'Express Allocation'

    if request.method == 'POST':
        form = PackageLevelForm(request.POST)
        form.set_package_levels(package_rows)
        if form.is_valid():
            if not request.session.get('new_product', None):
                request.session['new_product'] = {'gtin': str(prefix.starting_from),
                                         'package_level': form.data['package_level']}
            elif request.session.get('new_product')['gtin'] != str(prefix.starting_from):
                request.session['new_product'] = {'gtin': str(prefix.starting_from),
                                         'package_level': form.data['package_level']}
            else:
                request.session['new_product']['package_level'] = form.data['package_level']
            if express:
                request.session['new_product'].update({'express': True})
            elif 'express' in request.session['new_product']:
                del request.session['new_product']['express']
            return redirect(reverse('products:add_product_package_type'))
            # if session['new_product']['package_level'] == str(models.BASE_PACKAGE_LEVEL):
            #    if session['new_product'].get('express'):
            #        return redirect(url_for('products.add_product_express'))
            #    else:
            #        return redirect(url_for('products.add_product_package_type'))
            # else:
            #    return redirect(url_for('products.add_product_select_sub'))
        else:
            flash(request, 'You must choose a level to proceed', 'danger')
    else:
        form = PackageLevelForm()
        form.set_package_levels(package_rows)
        if ( request.session.get('new_product', None) and
             request.session.get('new_product')['gtin'] == str(prefix.starting_from) ):
            form.data['package_level'] = request.session.get('new_product')['package_level']

    context = { 'title': title,
               'prefix': prefix,
     'flashed_messages': flash_get_messages(request)
                }

    return render(request, 'products/package_level_form.html', context)


def products_list(request):
    return HttpResponse('products:products_list page')


def add_product_package_type(request):
    return HttpResponse('products:add_product_package_type')
