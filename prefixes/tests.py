from django.test import TestCase
from services import prefix_service
from BCM.models import Country
from member_organisations.models import MemberOrganisation


class PrefixesTestCase(TestCase):
    url = '/prefixes/'

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

    def test_models_make_starting_from(self):
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        prefix.make_starting_from()
        assert prefix.starting_from == '5390001100003'

    def test_models_get_active(self):
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert not prefix.is_active
        prefix_id = prefix.id
        prefix_organisation = prefix.company_organisation
        active_id=prefix_service.get_active(prefix_organisation)
        assert active_id is None
        prefix_service.make_active(prefix_id)
        active_id=prefix_service.get_active(prefix_organisation)
        assert active_id == prefix_id

    def test_ajax(self):
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert prefix.description == ''
        prefix_id = prefix.id
        response = self.client.post('/prefixes/ajax/', {'pk': prefix_id, 'value': 'New description'})
        assert response.status_code == 200
        assert response.content == b'{"success": true}'
        prefix = prefix_service.find(prefix='53900011').first()
        assert prefix.prefix == '53900011'
        assert prefix.description == 'New description'
