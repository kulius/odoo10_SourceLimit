# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


# Copyright (C) 2014-now  Jason Wu (jaronemo@msn.com)

{
    'name': '台灣 國際財務報導準則(IFRS)之會計科(項)目表',
    'version': '1.0',
    'category': 'Localization',
    'author': 'Jason Wu(jaronemo@msn.com)',
    'maintainer': 'Jason Wu(jaronemo@msn.com)',
    'website': 'http://www.osstw.com',
    'description': """

    參照  2016 / 05 台灣 國際財務報導準則(IFRS)之會計科(項)目表 更新事項

    """,
    'depends': ['account'],
    'data': [
        'data/l10n_tw_chart_data.xml',
        'data/account.account.template.csv',
        'data/account.tax.template.xml',
        'data/account_chart_template_data.xml',
        'data/account_chart_template_data.yml',
    ],
    'license': 'GPL-3',
}
