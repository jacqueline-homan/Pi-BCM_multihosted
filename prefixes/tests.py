from django.test import TestCase
from services import prefix_service


class PrefixesTestCase(TestCase):
    url = '/prefixes/'

    def setUp(self):
        post_data = {'uuid': '53900011',
                     'email': '53900011@test.com',
                     'company_prefix': '53900011,53900012',
                     'company_name': 'GS1 Ireland',
                     'credits': '39:20,43:100,44:100',
                     'txn_ref': 'Test_1,Test_3,Test_2'}
        self.client.post('/API/v1/AccountCreateOrUpdate/', post_data)

    def test_page_exist(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, 'Prefix management')

    def test_range_field(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, '<b>53900011</b><span style="color:#F26334">0000</span>3')
        self.assertContains(response, '<b>53900011</b><span style="color:#F26334">9999</span>1')
        self.assertContains(response, '<b>53900012</b><span style="color:#F26334">0000</span>0')
        self.assertContains(response, '<b>53900012</b><span style="color:#F26334">9999</span>8')

    def test_next_number_field(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertNotContains(response, '<b>53900011</b><span style="color:#F26334">0002</span>7')
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        prefix.starting_from = '5390001100027'
        prefix.save()
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert prefix.starting_from == '5390001100027'
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, '<b>53900011</b><span style="color:#F26334">0002</span>7')

    def test_no_suspendet_prefixes(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertNotContains(response, 'Suspended prefixes')

    def test_suspended_prefixes_exist(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        prefix.is_suspended = 1
        prefix.save()
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert prefix.is_suspended == 1
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, 'Suspended prefixes')
        self.assertContains(response, '<td>53900011</td>')

    def test_make_active(self):
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert not prefix.is_active
        id1 = prefix.id
        prefix = prefix_service.find(prefix='53900012').first()
        assert prefix.prefix == '53900012'
        assert not prefix.is_active
        id2 = prefix.id
        prefix_service.make_active(id1)
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert prefix.is_active
        prefix = prefix_service.find(prefix='53900012').first()
        assert prefix.prefix == '53900012'
        assert not prefix.is_active
        prefix_service.make_active(id2)
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert not prefix.is_active
        prefix = prefix_service.find(prefix='53900012').first()
        assert prefix.prefix == '53900012'
        assert prefix.is_active
