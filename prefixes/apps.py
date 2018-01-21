from django.apps import AppConfig


class PrefixesConfig(AppConfig):
    name = 'prefixes'


def template_context_processor(request):

    def get_range_data():
        from services import prefix_service
        prefix = prefix_service.get(1)
        if not prefix:
            return ''
        if prefix.is_upc():
            prfx = prefix.prefix[1:]
        else:
            prfx = prefix.prefix

        #prdcts = product_service.find(owner=user, gs1_company_prefix=prefix.prefix).all()
        prdcts = []
        prfxs = prefix.get_available_gtins(prdcts, True)

        #locations = location_service.find(owner=user, gs1_company_prefix=prefix.prefix).all()
        locations = []
        prfxs2 = prefix.get_available_glns(locations, True)

        return prfx, len(prdcts), prfxs, len(locations), prfxs2

    return {'get_range_data': get_range_data}
