from django.test import TestCase

from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase


class MOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'mo_admin'
    group_name = 'MO Admins'

    def setUp(self):
        super().setUp()
