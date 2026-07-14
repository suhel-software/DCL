# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleCustom(WebsiteSale):
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(attrib_set, options, post, search, website)
        
        if search_result:
            # Stable sort: in-stock first (qty_available > 0), out-of-stock last (qty_available <= 0)
            # Boolean True (out-of-stock) is placed after False (in-stock)
            search_result = search_result.sorted(
                key=lambda t: (
                    t.type == 'product' and t.qty_available <= 0
                )
            )
            
        return fuzzy_search_term, product_count, search_result
