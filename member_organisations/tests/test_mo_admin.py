from django.test import TestCase

from member_organisations.custom_admin.base_admin_tests import BaseAdminTestCase


class MOAdminTestCase(BaseAdminTestCase, TestCase):
    url_prefix = 'mo_admin'
    group_name = 'MO Admins'

    def setUp(self):
        super().setUp()

    # todo: adding tests for all available models (add urls)
    # todo: changing tests for all available models (change urls)
    # todo: deleting tests for all available models (delete urls)
    # todo: allowed/not allowed related model querysets/instances for admin-specific models
