from django.test import TestCase
from .apps import subproducts_reset


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

