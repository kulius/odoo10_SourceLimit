# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PackChoice(models.Model):
    _name = 'pack.choice'

    order_id = fields.Many2one(comodel_name='sale.order')
    choice_pack = fields.Many2one(comodel_name='product.product', string='選擇Bundle',
                                  domain=[('categ_id.name', '=', u'產品組合')])
    pack_amouny = fields.Integer(string='數量', default=1)

    def confirm(self):
        self.order_id.update_order_line(self.choice_pack, self.pack_amouny)
        return True
