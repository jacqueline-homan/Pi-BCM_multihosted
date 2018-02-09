from django.contrib.admin import AdminSite
from django.test import TestCase
from django.urls import reverse

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
from products.models.product import Product


class GOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'mo_admin'
    group_name = 'MO Admins'

    # todo: deleting instances tests for all available models (delete urls)
    # todo: allowed/not allowed related model querysets/instances for admin-specific models

    def setUp(self):
        super().setUp()
        self.model_instances = self.create_required_instances()

    def create_required_instances(self):
        user11 = self.create_django_user(self.main_user_credentials)
        user12 = self.create_django_user()
        user21 = self.create_django_user()

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

        mo1_user1 = self.mixer.blend(MemberOrganisationUser, organization=mo1, user=user11)
        mo1_user2 = self.mixer.blend(MemberOrganisationUser, organization=mo1, user=user12)
        mo2_user1 = self.mixer.blend(MemberOrganisationUser, organization=mo2, user=user21)

        mo_owner1 = self.mixer.blend(
            MemberOrganisationOwner, organization_user=mo1_user1, organization=mo1
        )
        mo_owner2 = self.mixer.blend(
            MemberOrganisationOwner, organization_user=mo2_user1, organization=mo2
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

        co1_user1 = self.mixer.blend(
            CompanyOrganisationUser,
            user=user11, organization=co1, is_admin=True,
        )

        co2_user1 = self.mixer.blend(
            CompanyOrganisationUser,
            user=user21, organization=co2, is_admin=True,
        )

        return {
            key: value for key, value in locals().items()
            if key[-1].isdigit()
        }

    def test_access_for_mo_admin_co(self):
        """
        mo1_user1 should be able to view companies in his MOs
        """

        login_result = self.client.login(**self.main_user_credentials)
        self.assertTrue(login_result, 'Can\'t login with test user credentials')

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

    def test_change_co_for_mo_admin(self):
        """
        mo1_user1 should be able to change companies with his MOs
        """

        login_result = self.client.login(**self.main_user_credentials)
        self.assertTrue(login_result, 'Can\'t login with test user credentials')

        test_co = self.model_instances['co1']
        post_data = self.model_instance_to_post_data(test_co)
        post_data['phone'] = '1111222233334444'  # field which will be changed

        co_url = self.get_url_for_model(CompanyOrganisation, 'change', test_co.pk)

        # instance creating is here
        response = self.client.post(co_url, data=post_data)

        self.assertEqual(
            response.status_code, 302, 'Should be a redirect after an instance submitting'
        )

        self.assertEqual(
            response.url,
            self.get_url_for_model(CompanyOrganisation, 'changelist'),
            f'Wrong redirect url after an instace updating'
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

    def test_delete_co_for_mo_admin(self):
        """
        mo1_user1 should be able to change companies with his MOs
        """

        login_result = self.client.login(**self.main_user_credentials)
        self.assertTrue(login_result, 'Can\'t login with test user credentials')

        test_co = self.model_instances['co1']
        post_data = {'post': 'yes'}

        self.assertTrue(
            CompanyOrganisation.objects.filter(
                company=test_co.company,
                member_organisation=test_co.member_organisation,
                country=test_co.country
            ).exists(),
            f'CompanyOrganisation "{test_co}" must be in the test database before deleting'
        )

        co_url = self.get_url_for_model(CompanyOrganisation, 'delete', test_co.pk)

        # instance creating is here
        response = self.client.post(co_url, data=post_data)

        self.assertEqual(
            response.status_code, 302, 'Should be a redirect after an instance submitting'
        )

        self.assertEqual(
            response.url,
            self.get_url_for_model(CompanyOrganisation, 'changelist'),
            f'Wrong redirect url after an instace removing'
        )

        self.assertFalse(
            CompanyOrganisation.objects.filter(
                company=test_co.company,
                member_organisation=test_co.member_organisation,
                country=test_co.country
            ).exists(),
            f'CompanyOrganisation "{test_co}" must be removed here already'
        )

    def test_add_models_for_mo_admin(self):
        """
        Test all models for adding instances
        :return:
        """

        login_result = self.client.login(**self.main_user_credentials)
        self.assertTrue(login_result, 'Can\'t login with test user credentials')

        models = {
            CompanyOrganisation: {
                'predefined_fields': {
                    'company': 'New test company',
                    'member_organisation': self.model_instances['mo1'],
                    'country': self.model_instances['mo1'].country,
                    'active': True
                }
            },
            CompanyOrganisationOwner: {
                'predefined_fields': {
                    'organization': self.model_instances['co1'],
                    'organization_user': self.model_instances['co1_user1'],
                }
            },
            CompanyOrganisationUser: {
                'predefined_fields': {
                    'user': self.model_instances['user12'],
                    'organization': self.model_instances['co1'],
                }
            },
            Prefix: {
                'predefined_fields': {
                    'company_organisation': self.model_instances['co1'],
                    'member_organisation': self.model_instances['mo1'],
                }
            },
            Product: None,  # too many new relations without description, skipped for now
            Log: {
                'predefined_fields': {}
            }
        }

        # alternative WRONG way to test without TestClient requests
        # This case django admin will use DEFAULT DATABASE (NOT A TEST ONE)
        # request = self.request_factory.get(reverse('admin:mo_admin'))
        # request.user = self.user
        # co_mo_admin_view = CompanyOrganisationCustomAdmin(CompanyOrganisation, AdminSite())
        # co_form_class = co_mo_admin_view.get_form(request)
        # co_form = co_form_class(data=post_data)
        # co_form.is_valid()
        # co_form.save()

        for model_class, model_conf in models.items():
            if not model_conf:
                continue

            predefined_fields = model_conf.get('predefined_fields', {})

            model_fields = self.get_force_random_fields_for_mixer(model_class, **predefined_fields)
            model_instance = self.mixer.blend(model_class, **model_fields)
            model_instance.delete()  # it seems mixer doesn't care about his commit=False
            post_data = self.model_instance_to_post_data(model_instance)

            self.assertFalse(
                model_class.objects.filter(**predefined_fields).exists(),
                f'CompanyOrganisation "{model_instance}" mustn\'t be '
                f'in the test database before submitting'
            )

            # instance creating is here
            model_add_url = self.get_url_for_model(model_class, 'add')
            response = self.client.post(model_add_url, data=post_data)

            self.assertEqual(
                response.status_code, 302, 'Should be a redirect after an instance submitting'
            )

            self.assertEqual(
                response.url,
                self.get_url_for_model(model_class, 'changelist'),
                f'Wrong redirect url after an instace adding'
            )

            self.assertTrue(
                model_class.objects.filter(**predefined_fields).exists(),
                f'CompanyOrganisation "{model_instance}" must be '
                f'in the test database after submitting'
            )











