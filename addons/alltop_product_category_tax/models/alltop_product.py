# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InheritProductCategory(models.Model):
    _inherit = 'product.category'

    product_tax_batch = fields.Many2many(comodel_name='account.tax',company_dependent=True, copy=True, string='分類銷售稅')

    def set_all_category_product(self):
        company = self.env.user.company_id
        tax = None
        if company.parent_id.id > 0:
            tax = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('price_include', '=', True)])
        elif len(company.child_ids) > 0:
            tax = self.env['account.tax']
            for line in company.child_ids:
                row = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('price_include', '=', True),
                                                      ('company_id', '=', line.id)])
                tax += row

        if tax is None:
            raise ValidationError(u'錯誤')
        for line in self.env['product.template'].search([('categ_id','=',self.id)]):
            line.taxes_id = tax

    def set_category_product_tax(self):
        tax = 0



