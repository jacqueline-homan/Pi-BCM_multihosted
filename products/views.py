from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from services import prefix_service
from core import flash
from .apps import subproducts_reset


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
        return redirect(reverse('prefixes.prefixes_list'))
    if not prefix.starting_from:
        flash('You must have a starting number set to enter new product. Please set one', 'danger')
        return redirect(reverse('prefixes.prefixes_list'))
    if prefix.is_special == 'READ-ONLY':
        flash('You can not add a new product in this range. It\'s a suspended read-only range', 'danger')
        return redirect(reverse('products.products_list'))

    return HttpResponse('products:add_product page')
