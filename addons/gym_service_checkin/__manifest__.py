# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Gym_Service_checkin_new',
    'version': '1.0',
    'category': 'Gym',
    'sequence': 2,
    'summary': '學員課程簽到',
    'description': """
            依銷售訂單中的課程，提供學員簽到及教練執行
            """,
    'author': 'kulius',
    'website': 'https://www.alltop.com.tw',
    'depends': [
        'base',
        'sale',
        'stock'
    ],
    'data': [
        'views/product_template_view.xml',
        'views/service_checkin_view.xml',

        'views/service_class_view.xml',
        'views/service_checkin_list_view.xml',
        'views/res_partner_inherit.xml',
        'views/account_invoice_inherit.xml',
        'views/menu.xml',

        'security/ir.model.access.csv',
    ],
    'demo': [],
    'images': [],
    'css': [],
    'installable': True,
    'application': True,
}
