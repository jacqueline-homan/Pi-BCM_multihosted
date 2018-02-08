import json

from mixer.backend.django import mixer

from django.contrib.auth.models import Group, User
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from member_organisations.admin import MemberOrganisationOwnerAdmin
from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase
from member_organisations.mo_admin.mo_views import CompanyOrganisationCustomAdmin

from member_organisations.models import (
    MemberOrganisation, MemberOrganisationUser, MemberOrganisationOwner
)
from company_organisations.models import (
    CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser
)
from BCM.models import Country, Language, LanguageByCountry
from audit.models import Log
from prefixes.models import Prefix
from products.models import Product


class GOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'mo_admin'
    group_name = 'MO Admins'

    # todo: deleting instances tests for all available models (delete urls)
    # todo: allowed/not allowed related model querysets/instances for admin-specific models

    def setUp(self):
        super().setUp()
        self.model_instances = self.create_member_organizations()

    def create_member_organizations(self):
        mo1 = self.mixer.blend(
            MemberOrganisation,
            name='GS1 France',
            country=Country.objects.get(name='France')
        )
        mo2 = self.mixer.blend(
            MemberOrganisation,
            name='GS1 Belgium',
            country=Country.objects.get(name='Belgium')
        )

        mo_user1 = self.mixer.blend(MemberOrganisationUser, organization=mo1, user=self.user)
        mo_user2 = self.mixer.blend(MemberOrganisationUser, organization=mo2)

        mo_owner1 = self.mixer.blend(
            MemberOrganisationOwner, organization_user=mo_user1, organization=mo1
        )
        mo_owner2 = self.mixer.blend(
            MemberOrganisationOwner, organization_user=mo_user2, organization=mo2
        )

        co_fields = self.get_force_random_fields_for_mixer(
            CompanyOrganisation,
            company='CO1 Test',
            member_organisation=mo1,
            country=mo1.country,
            active=True
        )
        co1 = self.mixer.blend(CompanyOrganisation, **co_fields)

        co_fields = self.get_force_random_fields_for_mixer(
            CompanyOrganisation,
            company='CO2 Test',
            member_organisation=mo2,
            country=mo2.country,
            active=True
        )
        co2 = self.mixer.blend(CompanyOrganisation, **co_fields)

        return {
            key: value for key, value in locals().items()
            if key[-1].isdigit()
        }

    def test_access_for_mo_admin_co(self):
        """
        mo_user1 should be able to view companies in his MOs
        """

        login_result = self.client.login(**self.user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        co_url = self.get_url_for_model(
            CompanyOrganisation, 'change', self.model_instances['co1'].pk
        )
        response = self.client.get(co_url)
        self.assertEqual(
            response.status_code, 200,
            f'URL "{co_url}" should be allowed for mo1 user'
        )

        co_url = self.get_url_for_model(
            CompanyOrganisation, 'change', self.model_instances['co2'].pk
        )
        response = self.client.get(co_url)
        self.assertEqual(
            response.status_code, 302,
            f'URL "{co_url}" should be denied for mo1 user'
        )

    def test_add_co_for_mo_admin(self):
        """
        mo_user1 should be able to add companies with his MOs
        """

        # alternative WRONG way to test without TestClient requuests
        # This case django admin will use DEFAULT DATABASE (NOT A TEST ONE)
        # request = self.request_factory.get(reverse('admin:mo_admin'))
        # request.user = self.user
        # co_mo_admin_view = CompanyOrganisationCustomAdmin(CompanyOrganisation, AdminSite())
        # co_form_class = co_mo_admin_view.get_form(request)
        # co_form = co_form_class(data=post_data)
        # co_form.is_valid()
        # co_form.save()

        login_result = self.client.login(**self.user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        co_fields = self.get_force_random_fields_for_mixer(
            CompanyOrganisation,
            company='New test company',
            member_organisation=self.model_instances['mo1'],
            country=self.model_instances['mo1'].country,
            active=True
        )

        new_co1 = self.mixer.blend(CompanyOrganisation, **co_fields)
        new_co1.delete()  # it seems mixer doesn't care about his commit=False
        post_data = self.model_instance_to_post_data(new_co1)

        co_url = self.get_url_for_model(CompanyOrganisation, 'add')

        self.assertFalse(
            CompanyOrganisation.objects.filter(
                company=co_fields['company'],
                member_organisation=self.model_instances['mo1'],
                country=self.model_instances['mo1'].country
            ).exists(),
            f'CompanyOrganisation "{new_co1}" must not be in the test database before submitting'
        )

        # instance creating is here
        response = self.client.post(co_url, data=post_data)

        self.assertEqual(
            response.status_code, 302, 'Should be a redirect after an instance submitting'
        )

        self.assertTrue(
            CompanyOrganisation.objects.filter(
                company=co_fields['company'],
                member_organisation=self.model_instances['mo1'],
                country=self.model_instances['mo1'].country
            ).exists(),
            f'CompanyOrganisation "{new_co1}" must be in the test database after submitting'
        )

    def test_change_co_for_mo_admin(self):
        """
        mo_user1 should be able to change companies with his MOs
        """

        login_result = self.client.login(**self.user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        test_co = self.model_instances['co1']
        post_data = self.model_instance_to_post_data(test_co)
        post_data['phone'] = '1111222233334444'  # field which will be changed

        co_url = self.get_url_for_model(CompanyOrganisation, 'change', test_co.pk)

        # instance creating is here
        response = self.client.post(co_url, data=post_data)

        self.assertEqual(
            response.status_code, 302, 'Should be a redirect after an instance submitting'
        )

        self.assertTrue(
            CompanyOrganisation.objects.filter(
                company=test_co.company,
                phone=post_data['phone'],  # must be updated in the test database
                member_organisation=self.model_instances['mo1'],
                country=self.model_instances['mo1'].country
            ).exists(),
            f'CompanyOrganisation "{test_co}" must have updated phone number'
        )
