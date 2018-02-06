from django.test import TestCase

from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase


class GOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'go_admin'
    group_name = 'GO Admins'

    def setUp(self):
        super().setUp()
