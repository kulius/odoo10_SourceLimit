# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    get_in_account_id = fields.Many2one('account.account', company_dependent=True,
                                        string="銷帳科目", domain=[('deprecated', '=', False)])


class InheritCateg(models.Model):
    _inherit = 'product.category'

    get_in_account_id = fields.Many2one('account.account', company_dependent=True,
                                        string="銷帳科目", domain=[('deprecated', '=', False)])