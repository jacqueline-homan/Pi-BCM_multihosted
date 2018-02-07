from mixer.backend.django import mixer

from django.contrib.auth.models import Group, User
from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from member_organisations.admin import MemberOrganisationOwnerAdmin
from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase

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

    # todo: adding instances tests for all available models (add urls)
    # todo: changing instances tests for all available models (change urls)
    # todo: deleting instances tests for all available models (delete urls)
    # todo: allowed/not allowed related model querysets/instances for admin-specific models

    def setUp(self):
        super().setUp()
        self.model_instances = self.create_member_organizations()

    def create_member_organizations(self):
        mo1 = mixer.blend(
            MemberOrganisation,
            name='GS1 France',
            country=Country.objects.get(name='France')
        )
        mo2 = mixer.blend(
            MemberOrganisation,
            name='GS1 Belgium',
            country=Country.objects.get(name='Belgium')
        )

        mo_user1 = mixer.blend(MemberOrganisationUser, organization=mo1, user=self.user)
        mo_user2 = mixer.blend(MemberOrganisationUser, organization=mo2)

        mo_owner1 = mixer.blend(
            MemberOrganisationOwner, organization_user=mo_user1, organization=mo1
        )
        mo_owner2 = mixer.blend(
            MemberOrganisationOwner, organization_user=mo_user2, organization=mo2
        )

        co1 = mixer.blend(CompanyOrganisation, member_organisation=mo1, country=mo1.country)
        co2 = mixer.blend(CompanyOrganisation, member_organisation=mo2, country=mo2.country)

        return {
            key: value for key, value in locals().items()
            if key[-1].isdigit()
        }

    def test_access_for_mo_admin_co(self):
        login_result = self.client.login(**self.user_credentials)
        self.assertTrue(login_result, 'Can\'t login to with test user credentials')

        co_url = self.get_url_for_model_instance(self.model_instances['co1'], 'change')
        response = self.client.get(co_url)
        self.assertEqual(
            response.status_code, 200,
            f'URL "{co_url}" should be allowed for mo1 user'
        )

        co_url = self.get_url_for_model_instance(self.model_instances['co2'], 'change')
        response = self.client.get(co_url)
        self.assertEqual(
            response.status_code, 302,
            f'URL "{co_url}" should be denied for mo1 user'
        )
