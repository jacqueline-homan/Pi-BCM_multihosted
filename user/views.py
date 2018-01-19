from django.http import HttpResponse
from django.shortcuts import render


def profile(request):
    current_user = {
        'active': True,
        'organisation': {
            'active': True,
            'credit_points_balance': 16,
        }
    }
    prefixes = [
        { 'id': '53900011',
          'get_capacity': 10000
        },
        { 'id': '53900012',
          'get_capacity': 10000
        },
    ]
    context = {
        'current_user': current_user,
        'alerts': True,
        'terms_alert': True,
        'terms_version': '2017/11/04',
        'uuid': '53900011',
        'company_name': 'GS1 Ireland',
        'prefixes': prefixes
    }
    return render(request, 'user/profile.html', context)


def products_add_product(request):
    return HttpResponse('products.add_product page')


def products_products_list(request):
    return HttpResponse('products.products_list page')


def static_views_terms(request):
    return HttpResponse('products.products_list page')


def prefixes_prefixes_list(request):
    return HttpResponse('prefixes.prefixes_list page')
