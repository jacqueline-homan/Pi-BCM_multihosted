from django.test import TestCase
from .apps import subproducts_reset
from BCM.models import Country
from member_organisations.models import MemberOrganisation


class ProductsTestCase(TestCase):
    def test_subproducts_reset(self):
        session = {}
        assert subproducts_reset(session) is None
        assert session == {}
        session = { 'new_product' : {} }
        assert subproducts_reset(session) is None
        assert session['new_product']['sub_products'] == []
        session = { 'new_product' : { 'sub_products' : ['sub_product1', 'sub_product2'] } }
        assert subproducts_reset(session) is None
        assert session['new_product']['sub_products'] == []


class ProductsAddProductTestCase(TestCase):
    url = '/products/add_product/'

    post_data = {       'uuid': '53900011',
                       'email': '53900011@test.com',
              'company_prefix': '53900011,53900012',
                'company_name': 'GS1 Ireland',
                     'credits': '39:20,43:100,44:100',
                     'txn_ref': 'Test_1,Test_3,Test_2',
         'member_organisation': 'gs1' }

    def setUp(self):
        country = Country(slug='BE', name='Belgium')
        country.save()
        member_organisation = MemberOrganisation(name='GS1',
                                                 slug='gs1',
                                                 is_active=1,
                                                 country=country)
        member_organisation.save()
        response = self.client.post('/API/v1/AccountCreateOrUpdate/', self.post_data)
        self.client.get(response.url)

    def test_page_exist(self):
        response = self.client.get(self.url + '?prefix=53900011')
        assert response.status_code == 200
        self.assertContains(response, 'New Product')
        self.assertContains(response, 'Packaging Level')

    def test_no_prefix_provided(self):
        response = self.client.get(self.url)
        assert response.status_code == 302
        assert response.url == '/prefixes/'

    def test_prefix_by_post(self):
        response = self.client.post(self.url, { 'prefix' : '53900011' })
        assert response.status_code == 200
        self.assertContains(response, 'New Product')
        self.assertContains(response, 'Packaging Level')

    def test_title_express(self):
        response = self.client.get(self.url + '?prefix=53900011')
        assert response.status_code == 200
        self.assertContains(response, 'New Product')
        response = self.client.get(self.url + '?prefix=53900011&express=1')
        assert response.status_code == 200
        self.assertContains(response, 'Express Allocation')
        response = self.client.post(self.url, { 'prefix': '53900011', 'express': 1 })
        self.assertContains(response, 'Express Allocation')
