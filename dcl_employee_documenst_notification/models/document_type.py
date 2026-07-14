# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DclDocumentType(models.Model):
    _name = 'dcl.document.type'
    _description = 'DCL Document Type'
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True, help="Name")
    sequence = fields.Integer(string='Sequence', default=10)
