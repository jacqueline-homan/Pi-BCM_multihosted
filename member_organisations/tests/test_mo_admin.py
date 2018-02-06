from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory
from django.urls import reverse

from BCM.models import Country


class PrefixesTestCase(TestCase):

    fixtures = (
        'fixtures/countries.json',
    )

    def setUp(self):
        super().setUp()

    def test_group_autocreation(self):
        # from django.db import connection
        # a = connection.settings_dict
        # print(f'test connections: {a}')
        # url = reverse('admin:mo_admin')
        # print(url)
        # response = self.client.get(url)
        # print(Group.objects.all())
        pass
