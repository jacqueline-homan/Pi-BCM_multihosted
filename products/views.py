from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404
from django.conf import settings
from services import prefix_service
from core import flash, flash_get_messages
from .apps import subproducts_reset
from .forms import PackageLevelForm, PackageTypeForm, ProductDetailForm
from .models.package_level import PackageLevel
from .models.package_type import PackageType
from .models.product import Product
from barcoding.utilities import normalize


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


def add_product_package_type(request):
    """
    package type selector
    :return:
    """
    session = request.session.get('new_product', None)
    if not session:
        raise Http404('Session does not exist')
    gtin = session.get('gtin', None)
    if not gtin:
        raise Http404('No gtin in session')
    prefix = prefix_service.find_item(starting_from=str(gtin))
    if not prefix:
        raise Http404('Starting prefix (%s) not found' % prefix)
    package_types = PackageType.service.filter(ui_enabled=True).order_by('id').all()

    if request.method == 'POST':
        form = PackageTypeForm(request.POST)
        form.set_package_types(package_types)
        if form.is_valid():
            request.session['new_product'].update({
                'package_type': form.data['package_type'],
                'bar_placement': form.bar_placement.data
            })
            if session.get('package_level') == '70':
                return redirect(reverse('products:add_product_base_details'))
            else:
                return redirect(reverse('products:add_product_select_sub'))
    else:
        form = PackageTypeForm()
        form.set_package_types(package_types)
        if session.get('package_level') == '70':
            form.bar_placement.data = settings.STATIC_URL + 'products/site/wizard/proddesc/BG.png'
            form.data['package_type'] = '1'
        else:
            form.bar_placement.data = settings.STATIC_URL + 'products/site/wizard/proddesc/CS.png'
            form.data['package_type'] = '34'

    if session.get('package_level') == '70':
        package_level = 'Base Unit / Each'
    elif session.get('package_level') == '60':
        package_level = 'Pack or inner pack'
    elif session.get('package_level') == '50':
        package_level = 'Case or mixed case'
    elif session.get('package_level') == '40':
        package_level = 'Display unit'
    else:
        package_level = 'Pallet' # 30

    context = { 'form': form,
              'prefix': prefix,
       'package_types': package_types,
       'package_level': package_level
                }
    return render(request, 'products/package_type_form.html', context=context)


def add_product_base_details(request):
    """
     -- used for the NEW (Step 2 - EACH)
    GET / POST for adding a base level item
    :template_name: products/product_details_form.html
    :return:
    """

    template_name = "products/product_details_form.html"

    session = request.session.get('new_product', None)
    if not session:
        raise Http404()
    for k in ['package_type', 'package_level', 'gtin', 'bar_placement']:  # Check session and restart if missing
        if k not in session.keys():
            del request.session['new_product']
            flash(request, 'Add new product restarted #010', 'danger')
            return redirect(reverse('products:add_product'))

    gtin = session.get('gtin', '0')
    package_type = session.get('package_type')
    bar_placement = session.get('bar_placement')

    prefix = prefix_service.find_item(starting_from=str(gtin))
    if not prefix:
        raise Http404()
    if prefix.is_upc():
        kind = 'UPCA'
    else:
        kind = 'EAN13'
    title = 'New Base Unit / Each (Step 2 of 2: Details)'
    context = {          'prefix': prefix,
                          'gtin0': '0',
                         'gtin13': session['gtin'],
                          'title': title,
                           'kind': kind,
       'product_package_level_id': int(session['package_level']),
                    'leading_gln': normalize('EAN13', prefix.prefix) }

    if request.method == 'POST':
        product = Product.service.create( gtin = gtin,
                                         owner = current_user,
                                  organisation = current_user.organisation,
                                   description = form.description.data,
                              labelDescription = form.functional_name.data,
                                         brand = form.brand.data,
                                     sub_brand = form.sub_brand.data,
                               functional_name = form.functional_name.data,
                                       variant = form.variant.data,
                                      category = form.category.data,
                            gs1_company_prefix = prefix.prefix,
                               gs1_cloud_state = 'INACTIVE',
                              package_level_id = form.package_level_id.data,
                               package_type_id = int(package_type),
                                   net_content = form.net_content.data,
                               net_content_uom = form.net_content_uom.data,
                                                 # non-null fields
                                      language = form.language.data,
                                 target_market = form.target_market.data,
                             country_of_origin = form.country_of_origin.data,
                                       company = prefix.organisation.company )
    else:
        context['is_new'] = 1
        form = ProductDetailForm()
        # default values - new product GET
        form.initial['gln_of_information_provider'] = normalize('EAN13', prefix.prefix)
        form.initial['is_bunit'] = True
        form.initial['company'] = prefix.member_organisation.name
        # _add_field_descriptions(form)
        #form.process()

    context['form'] = form
    #form.bar_placement.data = session.get('bar_placement')
    #form.package_level_id.data = session.get('package_level')
    #form.package_type_id.data = session.get('package_type')
    #form.image.data = session.get('image', settings.NO_IMAGE)
    return render(request, 'products/product_details_form.html', context=context)


def products_list(request):
    return HttpResponse('products:products_list page')


def add_product_select_sub(request):
    return HttpResponse('products:add_product_select_sub')
