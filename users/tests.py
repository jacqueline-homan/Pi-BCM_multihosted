from django.test import TestCase
from services import prefix_service
from BCM.models import Country
from member_organisations.models import MemberOrganisation


class UsersTestCase(TestCase):
    url = '/profile/'

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
        response = self.client.get(response.url)
        pass

    def test_page_exist(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, 'Dashboard')

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

    def _test_terms_not_agreed(self):
        response = self.client.post(self.url, {'submit': 'Submit'})
        assert response.status_code == 200
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertContains(response, 'I agree to the Terms and Conditions')

    def test_terms_agreed(self):
        response = self.client.post(self.url, {'submit': 'Submit', 'agree': 'on'})
        assert response.status_code == 200
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertNotContains(response, 'I agree to the Terms and Conditions')

