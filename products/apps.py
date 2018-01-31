from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'


def subproducts_reset(session):
    """
    removes all previously selected subproducts from session
    :return:
    """
    if not session.get('new_product') is None:
        if not session['new_product'].get('sub_products'):
            session['new_product']['sub_products'] = []
        else:
            #for p in session['new_product']['sub_products']:
            #    session['new_product']['sub_products'].remove(p)
            session['new_product']['sub_products'] = []
