import tempfile
import json
from zipfile import ZipFile
from openpyxl import load_workbook
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from services import prefix_service, users_service
from .forms import PrefixActionForm
from products.models import Product


def prefixes_list(request):
    flashed_messages = []
    current_user = users_service.get(1)

    prefixes = prefix_service.all()
    susp_prefixes = prefix_service.find(organisation=current_user.organisation, is_suspended=True).all()

    '''
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

    if request.method == 'POST':
        form = PrefixActionForm(request.POST)
        form.fields['select_prefix'].choices = [(str(p.id), p.prefix) for p in prefixes]
        if form.is_valid():
            try:
                int_prefix_id = int(form.data['select_prefix'])
            except (ValueError, TypeError):
                flashed_messages.append(('Your selections were not valid!', 'danger'),)
            else:
                prefix = prefix_service.get(int_prefix_id)
                if not prefix:
                    raise Http404('Prefix not found')

                if prefix.is_special == 'READ-ONLY' and form.data['prefix_action'] != 'set_this':
                    flashed_messages.append(('Read-only prefix, please contact GS1 helpdesk.', 'danger'),)
                else:
                    prefix_service.make_active(prefix.id)

                    prefix_action = form.data['prefix_action']
                    # Enter a new product in selected range
                    if prefix_action == 'new_product':
                        return redirect(reverse('user:products.add_product') + '?prefix=' + str(prefix.prefix))

                    # Set selected range as active and go to My Products
                    elif prefix_action == 'set_this':
                        return redirect(reverse('user:products.products_list'))

                    # Set starting GTIN in selected range manually
                    elif prefix_action == 'starting_gtin':
                        return redirect(reverse('prefixes:prefixes_set_starting', args=(prefix.id,)))

                    # Set starting GTIN to first available number
                    elif prefix_action == 'first_available':
                        try:
                            prefix.make_starting_from()
                        except Exception as e:
                            return render(request, 'prefixes/prefix_exhausted.html',
                                                   {'current_user': current_user, 'prefix': prefix })
                        prefix_service.save(prefix)
                        return redirect(reverse('prefixes:prefixes_list'))

                    # new location
                    elif prefix_action == 'new_gln':
                        return redirect(reverse('user:locations.add_location') + '?prefix=' + str(prefix.prefix))

                    elif prefix_action == 'first_available_gln':
                        pass
                        '''
                        try:
                            prefix.make_starting_from_gln()
                        except Exception,e:
                            return render_template('prefixes/prefix_exhausted.html', prefix=prefix)
                        prefix_service.save(prefix)
                        return redirect(url_for('.prefixes_list'))
                        '''

                    # Export available GTINs in this range
                    elif prefix_action == 'export_available':
                        try:
                            products = ( Product.objects.filter(owner = current_user)
                                                        .filter(gs1_company_prefix = prefix.prefix)
                                                        .order_by('gtin') )
                            prfxs = prefix.get_available_gtins(products)
                            if len(prfxs) > 0:
                                tfile = tempfile.NamedTemporaryFile(suffix='.xlsx')
                                zfile = tempfile.NamedTemporaryFile(suffix='.zip')

                                file_xlsx = load_workbook(settings.PREFIXES_EXCEL_TEMPLATE)
                                ws = file_xlsx.get_active_sheet()
                                for index, prfx in enumerate(prfxs):
                                    _ = ws.cell(column=2, row=index + 5, value=prfx)
                                file_xlsx.save(filename=tfile.name)

                                with ZipFile(zfile.name, "w") as z:
                                    export_filename = "export_%s_available.xlsx" % (prefix.prefix,)
                                    attachment_filename = "export_%s_available.%s" % (prefix.prefix, 'zip')
                                    z.write(tfile.name, export_filename)

                                send_file = open(zfile.name, 'rb')
                                response = HttpResponse(send_file, content_type='application/zip')
                                response['Content-Disposition'] = 'attachment; filename=%s' % attachment_filename
                                return response
                            else:
                                flashed_messages.append(('There are no available GTIN numbers for current active prefix', 'danger'),)
                        except Exception as e:
                            flashed_messages.append(('Error: %s' % str(e), 'danger'),)
        else:
            flashed_messages.append(('You must choose a prefix and an action!', 'danger'),)

    form = PrefixActionForm()
    form.fields['select_prefix'].choices = [(str(p.id), p.prefix) for p in prefixes]
    try:
        selected_prefix = int(request.POST['select_prefix'])
        prefix_service.make_active(selected_prefix)
    except:
        selected_prefix = prefix_service.get_active(current_user.organisation)

    config = {'GS1_GLN_CAPABILITY': settings.GS1_GLN_CAPABILITY}

    context = {
        'current_user': current_user,
        'config': config,
        'prefixes': prefixes,
        'susp_prefixes': susp_prefixes,
        'flashed_messages': flashed_messages,
        'selected_prefix': selected_prefix
    }
    return render(request, 'prefixes/prefixes_list.html', context)


def prefixes_set_starting(request, prefix_id):
    return HttpResponse('prefixes_set_starting: %s' % prefix_id)


def jsonify(**kwargs):
    content = json.dumps(kwargs)
    response = HttpResponse(content, content_type='application/json')
    response['Content-Length'] = len(content)
    return response


def prefixes_ajax(request):
    if request.method != 'POST':
        return Http404()
    current_user = users_service.get(1)
    prefix_id = request.POST.get('pk', None)
    if not prefix_id:
        return Http404()
    prefix = prefix_service.find_item(organisation=current_user.organisation, id=prefix_id)
    if not prefix:
        return Http404()
    prefix.description = request.POST.get('value', None)
    prefix_service.save(prefix)
    return jsonify(success=True)
