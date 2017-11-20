# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    taiwan_invoice = fields.Char(string='發票號碼')
    invoice_type = fields.Selection(selection=[(u'二聯', u'二聯'), (u'三聯', u'三聯')], string='發票類型', default=u'二聯')
