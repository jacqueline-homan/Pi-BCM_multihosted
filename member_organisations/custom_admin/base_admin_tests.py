from django.contrib.auth.models import Group, User
from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

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
    user_credentials = None
    user = None
    group = None

    fixtures = (
        'fixtures/bcm.json',
        'fixtures/groups.json',
    )

    def setUp(self):
        super().setUp()
        self.mo_admin_instance = MemberOrganisationOwnerAdmin(
            CompanyOrganisationOwner, admin.site
        )
        self.user_credentials = {
            'username': 'moadmin',
            'password': '1234',
        }
        self.user = User(**self.user_credentials)
        self.user.set_password(self.user_credentials['password'])
        self.user.save()
        self.group = Group.objects.get(name=self.group_name)
        self.user.groups.add(self.group)

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

    def get_url_for_model_instance(self, model_instance, action):
        app_label = model_instance._meta.model._meta.app_label
        model_name = model_instance._meta.model._meta.model_name

        return (reverse(
                f'admin:{self.url_prefix}_{app_label}_{model_name}_{action}',
                args=(model_instance.pk,)))

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

        login_result = self.client.login(**self.user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        url_names = self.get_urls_by_types(['changelist', 'add'])
        for url_name in url_names:
            response = self.client.get(url_name)
            self.assertEqual(
                response.status_code, 200,
                f'URL "{url_name}" should be allowed for authorized/authenticated users'
            )
