import json

from django.db.models import DateTimeField
from django.utils.dateparse import parse_datetime
from mixer.backend.django import Mixer
from django.contrib.auth.models import Group, User
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.test import RequestFactory
from django.urls import reverse
from django.core import serializers

from company_organisations.models import CompanyOrganisationOwner
from member_organisations.admin import MemberOrganisationOwnerAdmin


class BaseAdminTestCase(object):
    """
    We have to inherit from "object" here cause TestCase is something like singleton
    and if TestCase will be specified here, base class will be tested too with errors
    """

    url_prefix = None  # 'mo_admin' / 'go_admin'
    group_name = None  # 'MO Admins' / 'GO Admins'
    mo_admin_instance = None
    main_user_credentials = None
    group = None
    request_factory = None
    mixer = None

    fixtures = (
        'fixtures/bcm.json',
        'fixtures/groups.json',
    )

    def setUp(self):
        super().setUp()
        self.mo_admin_instance = MemberOrganisationOwnerAdmin(
            CompanyOrganisationOwner, AdminSite()
        )
        self.main_user_credentials = {
            'username': 'moadmin',
            'password': '1234',
        }
        self.group = Group.objects.get(name=self.group_name)
        self.request_factory = RequestFactory()
        self.mixer = Mixer(locale='en')

    def create_django_user(self, user_credentials=None, add_to_group=True):

        if user_credentials:
            user = User(**user_credentials)
            user.set_password(self.main_user_credentials['password'])
            user.save()
        else:
            user = self.mixer.blend(User)

        if add_to_group:
            user.groups.add(self.group)
        return user

    def get_force_random_fields_for_mixer(self, model_class, excluded_fields=('id',), **kwargs):
        """
        Mixer sets default values from model,
        but it raises errors when blank=False and default='' at the same time,
        so we have to force fields to be set by random values

        :param model_class:
        :param excluded_fields: ('id', )  # prevent to randomize some fields
        :param kwargs: field_name=instance or value  # predefined field values
        :return: dict of field_names: random/predefined values
        """

        co_fields = {
            field.name: self.mixer.RANDOM
            for field in model_class._meta.fields if field.name not in excluded_fields
        }

        for field_name, field_value in kwargs.items():
            co_fields[field_name] = field_value

        return co_fields

    @classmethod
    def model_instance_to_post_data(cls, instance):
        data = serializers.serialize('json', [instance, ])
        struct = json.loads(data)
        post_data = struct[0]['fields']

        for field in instance._meta.fields:
            # splitting date and time for admin forms
            if isinstance(field, DateTimeField):
                field_datetime = parse_datetime(post_data[field.name])
                post_data[f'{field.name}_0'] = str(field_datetime.date())
                post_data[f'{field.name}_1'] = str(field_datetime.time())
                del post_data[field.name]

        return post_data

    def get_urls_by_types(self, url_types):
        """
        Filters url list by types like: "changelist", "add", "change", "delete"
        """

        url_names = list()
        for url in self.mo_admin_instance.get_urls():
            if not url.name:
                continue
            if not url.name.startswith(self.url_prefix):
                continue

            if any(url_type in url.name for url_type in url_types):
                url_names.append(reverse(f'admin:{url.name}'))

        return url_names

    def get_url_for_model(self, model_class, action, pk=None):
        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name

        return (
            reverse(
                f'admin:{self.url_prefix}_{app_label}_{model_name}_{action}',
                args=(pk,) if pk else None))

    def test_changelist_add_urls_non_authorized_user(self):
        """
        Non authorized users must receive 302 http response to login page
        """

        url_names = self.get_urls_by_types(['changelist', 'add'])

        for url_name in url_names:
            response = self.client.get(url_name)
            self.assertEqual(
                response.status_code, 302,
                f'URL "{url_name}" should be denied for non authorized users'
            )

    def test_changelist_add_urls_authorized_user(self):
        """
        Authorized and authenticated users must receive 200 http response
        """

        login_result = self.client.login(**self.main_user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        url_names = self.get_urls_by_types(['changelist', 'add'])
        for url_name in url_names:
            response = self.client.get(url_name)
            self.assertEqual(
                response.status_code, 200,
                f'URL "{url_name}" should be allowed for authorized/authenticated users'
            )
