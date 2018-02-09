from django.test import TestCase

from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase


class GOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'go_admin'
    group_name = 'GO Admins'

    def setUp(self):
        super().setUp()
        self.model_instances = self.create_required_instances()

    def create_required_instances(self):
        user11 = self.create_django_user(self.main_user_credentials)
        user12 = self.create_django_user()
        user21 = self.create_django_user()
