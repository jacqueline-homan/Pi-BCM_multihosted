from django.http import HttpResponse
from django.shortcuts import render
from services import prefix_service
from django.conf import settings


def profile(request):
    current_user = {
        'active': True,
        'is_authenticated': True,
        'agreed': True,
        'organisation': {
            'active': True,
            'credit_points_balance': 16,
            'company': 'GS1 Ireland',
            'uuid': '53900011'
        }
    }

    prefixes = prefix_service.all()
    '''
    result = db.session.query('prefix', 'products').
        from_statement(text("select products.gs1_company_prefix as prefix, 
                                    count(*) as products
                             from products
                             where owner_id=%s
                             group by products.gs1_company_prefix" % current_user.id)).all()

    result_locations = db.session.query('prefix', 'locations'). \
        from_statement(text("select locations.gs1_company_prefix as prefix, 
                                    count(*) as locations
                             from locations
                             where owner_id=%s
                             group by locations.gs1_company_prefix" % current_user.id)).all()
                             
    # set products count
    for prefix in prefixes:
        for row in result:
            if prefix.prefix == row[0]:
                setattr(prefix, 'products', row[1])

    # set locations count
    for prefix in prefixes:
        for row in result_locations:
            if prefix.prefix == row[0]:
                setattr(prefix, 'locations', row[1])
    '''

    if request.method == 'POST':
        if request.form.get('agree'):
            pass
            '''
            current_user.agreed = True
            current_user.agreed_date = datetime.datetime.utcnow()
            current_user.agreed_version = current_app.config['TERMS_VERSION']
            db.session.add(current_user)
            db.session.commit()
            '''

    alerts = False
    terms_alert = False
    terms_version = settings.TERMS_VERSION

    if not current_user['agreed']:
        alerts = True
        terms_alert = True

    config = { 'GS1_GLN_CAPABILITY': settings.GS1_GLN_CAPABILITY }

    context = {
        'current_user': current_user,
        'config': config,
        'alerts': alerts,
        'terms_alert': terms_alert,
        'terms_version': terms_version,
        'uuid': '53900011',
        'company_name': current_user['organisation']['company'],
        'prefixes': prefixes,
    }
    if settings.DEBUG:
        context.update({ 'uuid': current_user['organisation']['uuid'] })  # For debug purposes

    return render(request, 'user/profile.html', context)


def products_add_product(request):
    return HttpResponse('products.add_product page')


def products_products_list(request):
    return HttpResponse('products.products_list page')


def static_views_terms(request):
    return HttpResponse('products.products_list page')


def prefixes_prefixes_list(request):
    return HttpResponse('prefixes.prefixes_list page')


def auth_profile(request):
    return HttpResponse('auth_profile page')


def excel_export_select(request):
    return HttpResponse('excel.export_select page')


def excel_import_file(request):
    return HttpResponse('excel.import_file page')


def locations_locations_list(request):
    return HttpResponse('locations.locations_list')
