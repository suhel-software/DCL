# -*- coding: utf-8 -*-

from odoo import models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
        # We run the computation with sudo() because public/portal users do not have read access to mrp.bom
        # and standard mrp computes kit quantities by querying mrp.bom._bom_find.
        if self.env.user._is_public() or self.env.user.has_group('base.group_portal'):
            return super(ProductProduct, self.sudo())._compute_quantities_dict(lot_id, owner_id, package_id, from_date=from_date, to_date=to_date)
        return super()._compute_quantities_dict(lot_id, owner_id, package_id, from_date=from_date, to_date=to_date)
