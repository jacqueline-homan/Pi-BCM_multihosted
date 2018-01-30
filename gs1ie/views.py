import logging
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, reverse
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from barcoding.utilities import normalize
from company_organisations.models import CompanyOrganisation
from member_organisations.models import MemberOrganisation
from services import users_service, prefix_service
from .forms import AccountCreateOrUpdateForm
from core import jsonify


# class User:
#    def is_authenticated(self):
#        return True


@transaction.atomic
def account_create_or_update(request):
    if request.method == 'POST':
        form = AccountCreateOrUpdateForm(request.POST)
        if form.is_valid():
            try:
                # core data
                email = form.data.get('email')
                company_name = form.data.get('company_name')
                try:
                    member_organisation = MemberOrganisation.objects.get(
                        slug=form.cleaned_data.get('member_organisation'))
                except MemberOrganisation.DoesNotExist:
                    member_organisation = None

                # get company
                company_organisation, company_organisation_created = CompanyOrganisation.objects.get_or_create(
                    uuid=form.data.get('uuid'),
                    member_organisation=member_organisation
                )

                # update company name if any
                if company_name:
                    company_organisation.company = company_name
                    company_organisation.save()

                auth_user, auth_user_created = users_service.get_or_create(email=email,
                                                             defaults={
                                                                 'username': email,
                                                                 'customer_role': 'gs1ie',
                                                                 'member_organisation': member_organisation,
                                                                 'company_organisation': company_organisation
                                                             })

                auth_user.save()

                company_organisation = users_service.get_company_organisation(auth_user)

                # user, user_created = users_service.get_or_create(email=email,
                #                                                  defaults={
                #                                                      'username': email,
                #                                                      'customer_role': 'gs1ie',
                #                                                      'organisation': organisation
                #                                                  })

            except Exception as e:
                return jsonify(success=False, message=str(e))

            log_message = 'logging in: ' + str(auth_user.email) + '::' + str(company_organisation.company)
            log_extra = {'user': auth_user.email,
                         'company': company_organisation.company,
                         'ip_address': request.environ.get('REMOTE_ADDR')}
            logging.getLogger().info(log_message, extra=log_extra)
            logging.getLogger('audit').info(log_message, extra=log_extra)

            # if user's organisation has prefix override, use it
            # if not use prefixes provided by the form
            if not company_organisation.prefix_override:
                form_prefix = form.data.get('company_prefix', '')
            else:
                form_prefix = company_organisation.prefix_override
            form_prefixes = form_prefix.split(',')

            prefixes = prefix_service.find(company_organisation=company_organisation,
                                           member_organisation=member_organisation).all()
            prefixes_list = [p.prefix for p in prefixes]

            # set gln to be first prefix
            if len(prefixes_list) > 0:
                first_prefix = prefixes_list[0]
                derived_gln = normalize("EAN13", first_prefix)
                company_organisation.gln = derived_gln
                company_organisation.save()

            for prfx in form_prefixes:
                if not re.match(settings.GS1_PREFIX_START_REGEX, prfx[:3]) or len(prfx) < 6:
                    if prfx.find('20') == 0:  # we will not complain about variable weight
                        continue
                    else:
                        return jsonify(success=False, message='Invalid prefix %s' % prfx)
                if prfx not in prefixes_list:
                    try:
                        prefix = prefix_service.create(prefix=prfx, company_organisation=company_organisation,
                                                       member_organisation=member_organisation)
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
                    prefix = prefix_service.find(company_organisation=company_organisation,
                                                 member_organisation=member_organisation, prefix=prfx).first()
                    prefix.is_suspended = True
                    prefix.is_active = False
                    prefix_service.save(prefix)

            # Check active prefix and set accordingly
            try:
                prefix_service.find(company_organisation=company_organisation, member_organisation=member_organisation,
                                    is_active=True, is_suspended=False).first()
            except ObjectDoesNotExist:
                prefix = prefix_service.find(company_organisation=company_organisation,
                                             member_organisation=member_organisation, is_active=False,
                                             is_suspended=False).order_by('prefix').first()
                if not prefix:
                    return jsonify(success=False, message='No working prefix found')
                prefix.is_active = True
                prefix_service.save(prefix)
            except MultipleObjectsReturned:
                prefixes = prefix_service.find(company_organisation=company_organisation,
                                               member_organisation=member_organisation, is_active=True,
                                               is_suspended=False).order_by('prefix').all()
                for prefix in prefixes:
                    prefix.is_active = False
                    prefix_service.save(prefix)
                prefix = prefixes[0]
                prefix.is_active = True
                prefix_service.save(prefix)

            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            token = serializer.dumps([auth_user.email, company_organisation.uuid])
            logging.getLogger().debug('Created token: %s' % token)
            return redirect('/API/v1/auth/%s/' % token)
    else:
        form = AccountCreateOrUpdateForm()

    current_user = request.user
    context = {'current_user': current_user,
               'active_page': '',
               'form': form}
    return render(request, 'gs1ie/AccountCreateOrUpdate.html', context)


def api_auth(request, token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        logging.getLogger().debug('Received token: %s' % token)
        email, uuid = serializer.loads(token, max_age=30)
    except SignatureExpired:
        return render(request, 'gs1ie/token_expired.html', status=403)
    user = users_service.find(email=email, customer_role='gs1ie')
    if not user:
        return render(request, 'gs1ie/user_not_found.html', status=404)

    login(request, user)

    #if user.login_count is None:
    #    login_count = 1
    #else:
    #    login_count = user.login_count + 1
    #users_service.update(user, login_count=login_count)

    return redirect(reverse('profile'))
