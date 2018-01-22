from django.shortcuts import render
from django.conf import settings
from services import prefix_service, users_service


def prefixes(request):
    current_user = {
        'id': 1,
        'active': True,
        'is_authenticated': True,
        'agreed': True,
        #'organisation': {
        #    'active': True,
        #    'credit_points_balance': 16,
        #    'company': 'GS1 Ireland',
        #    'uuid': '53900011'
        #}
    }

    current_user['organisation'] = users_service.get(current_user['id']).organisation

    prefixes = prefix_service.all()
    susp_prefixes = prefix_service.find(organisation=current_user['organisation'], is_suspended=True).all()
    #susp_prefixes = prefix_service.find(is_suspended=True).all()

    '''
    susp_prefixes = prefix_service.find(organisation=current_user.organisation, is_suspended=True).all()

    prefixes = prefix_service.find_all().all()
    result = db.session.query('prefix', 'products'). \
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

    config = {'GS1_GLN_CAPABILITY': settings.GS1_GLN_CAPABILITY}

    context = {
        'current_user': current_user,
        'config': config,
        'prefixes': prefixes,
        'susp_prefixes': susp_prefixes
    }
    return render(request, 'prefixes/prefixes_list.html', context)
