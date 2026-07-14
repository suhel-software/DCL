# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    global_document_expiry_recipient_ids = fields.Many2many(
        'hr.employee',
        string="HR Document Reminder Access",
        help="Select employees who should globally receive document expiry notification emails"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        recipient_ids_str = params.get_param('dcl_employee_documenst_notification.global_document_expiry_recipient_ids', '')
        if recipient_ids_str:
            recipient_ids = [int(x) for x in recipient_ids_str.split(',') if x.isdigit()]
            res.update(
                global_document_expiry_recipient_ids=[(6, 0, recipient_ids)]
            )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        recipient_ids = self.global_document_expiry_recipient_ids.ids
        recipient_ids_str = ','.join(map(str, recipient_ids))
        self.env['ir.config_parameter'].sudo().set_param(
            'dcl_employee_documenst_notification.global_document_expiry_recipient_ids',
            recipient_ids_str
        )
