import re
import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from services import organisation_service, users_service, prefix_service
from django.conf import settings
from barcoding.utilities import normalize
from .forms import AccountCreateOrUpdateForm


class User:
    def is_authenticated(self):
        return True


def jsonify(**kwargs):
    content = json.dumps(kwargs)
    response = HttpResponse(content, content_type='application/json')
    response['Content-Length'] = len(content)
    return response


@transaction.atomic
def account_create_or_update(request):
    if request.method == 'POST':
        form = AccountCreateOrUpdateForm(request.POST)
        if form.is_valid():
            try:
                # core data
                email = form.data.get('email')
                company = form.data.get('company_name')

                # get company
                organisation, organisation_created = organisation_service.get_or_create(
                    uuid=form.data.get('uuid'),
                    country=form.cleaned_data.get('country')
                )

                # update company name if any
                if company:
                    organisation_service.update(organisation, company=company)

                # get or create user
                user, user_created = users_service.get_or_create(email=email,
                                                                 defaults={
                                                                     'username': email,
                                                                     'customer_role': 'gs1ie',
                                                                     'organisation': organisation
                                                                 })
            except Exception as e:
                return jsonify(success=False, message=e.message)

            log_message = 'logging in: ' + str(user.email) + '::' + str(user.organisation.company)
            log_extra = { 'user': user.email,
                       'company': user.organisation.company,
                    'ip_address': request.environ.get('REMOTE_ADDR') }
            logging.getLogger().info(log_message, extra=log_extra)
            logging.getLogger('audit').info(log_message, extra=log_extra)

            # if user's organisation has prefix override, use it
            # if not use prefixes provided by the form
            if not organisation.prefix_override:
                form_prefix = form.data.get('company_prefix', '')
            else:
                form_prefix = organisation.prefix_override
            form_prefixes = form_prefix.split(',')

            prefixes = prefix_service.find(organisation=organisation).all()
            prefixes_list = [p.prefix for p in prefixes]

            # set gln to be first prefix
            if len(prefixes_list) > 0:
                first_prefix = prefixes_list[0]
                derived_gln = normalize("EAN13", first_prefix)
                organisation_service.update(organisation, gln=derived_gln)

            for prfx in form_prefixes:
                if not re.match(settings.GS1_PREFIX_START_REGEX, prfx[:3]) or len(prfx) < 6:
                    if prfx.find('20') == 0:  # we will not complain about variable weight
                        continue
                    else:
                        return jsonify(success=False, message='Invalid prefix %s' % prfx)
                if prfx not in prefixes_list:
                    try:
                        prefix = prefix_service.create(prefix=prfx, organisation=organisation)
                    except IntegrityError:
                        return jsonify(success=False, message='Prefix %s has been allocated for another user' % prfx)
                    try:
                        prefix.make_starting_from()
                    except:
                        prefix.starting_from = None
                    prefix_service.save(prefix)
                else:
                    i = prefixes_list.index(prfx)
                    if prefixes[i].is_suspended:
                        prefixes[i].is_suspended = False
                        prefix_service.save(prefixes[i])

            for prfx in prefixes_list:
                if prfx not in form_prefixes:
                    prefix = prefix_service.find(organisation=organisation, prefix=prfx).first()
                    prefix.is_suspended = True
                    prefix.is_active = False
                    prefix_service.save(prefix)

            # Check active prefix and set accordingly
            try:
                prefix_service.find(organisation=organisation, is_active=True, is_suspended=False).first()
            except ObjectDoesNotExist:
                prefix = prefix_service.find(organisation=organisation, is_active=False, is_suspended=False).order_by('prefix').first()
                if not prefix:
                    return jsonify(success=False, message='No working prefix found')
                prefix.is_active = True
                prefix_service.save(prefix)
            except MultipleObjectsReturned:
                prefixes = prefix_service.find(organisation=organisation, is_active=True, is_suspended=False).order_by('prefix').all()
                for prefix in prefixes:
                    prefix.is_active = False
                    prefix_service.save(prefix)
                prefix = prefixes[0]
                prefix.is_active = True
                prefix_service.save(prefix)

            form = AccountCreateOrUpdateForm()
    else:
        form = AccountCreateOrUpdateForm()

    current_user = User()
    context = { 'current_user': current_user,
                'active_page': '',
                'form': form }
    return render(request, 'gs1ie/AccountCreateOrUpdate.html', context)
