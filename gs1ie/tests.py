from django.test import TestCase

from BCM.models import Country
from member_organisations.models import MemberOrganisation
from services import organisation_service, users_service, prefix_service, logs_service


class Gs1IeTestCase(TestCase):
    url = '/API/v1/AccountCreateOrUpdate/'

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

    def test_page_exist(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_page_is_AccountCreateOrUpdate(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'AccountCreateOrUpdate')

    def test_page_post(self):
        response = self.client.post(self.url, self.post_data)
        assert response.status_code == 302

    def test_page_empty_post(self):
        response = self.client.post(self.url, {})
        assert response.status_code == 200
        self.assertContains(response, 'AccountCreateOrUpdate')

    #def test_organisation_data(self):
    #    self.client.post(self.url, self.post_data)
    #    organisation = organisation_service.find(uuid='53900011').first()
    #    assert organisation.uuid == '53900011'
    #    assert organisation.company == 'GS1 Ireland'

    #def test_users_data(self):
    #    self.client.post(self.url, self.post_data)
    #    users = users_service.all()
    #    assert len(users) == 1
    #    assert users[0].email == '53900011@test.com'
    #    assert users[0].customer_role == 'gs1ie'
    #    assert users[0].organisation.company == 'GS1 Ireland'

    def test_prefixes_data(self):
        self.client.post(self.url, self.post_data)
        prefixes = prefix_service.all()
        assert len(prefixes) == 2
        assert prefixes[0].prefix == '53900011'
        #assert prefixes[0].organisation.company == 'GS1 Ireland'
        assert prefixes[1].prefix == '53900012'
        #assert prefixes[1].organisation.company == 'GS1 Ireland'

    def test_audit_data(self):
        self.client.post(self.url, self.post_data)
        audit = logs_service.all()
        assert len(audit) == 1
        assert audit[0].logger == 'audit'
        assert audit[0].level == 'INFO'
        assert audit[0].msg == 'logging in: 53900011@test.com::GS1 Ireland'
        assert audit[0].username == '53900011@test.com'
