# -*- coding: utf-8 -*-

{
    'name': 'FFACSA WebServices',
    'version': '1.0.1',
    'author': 'Xetechs GT',
    'license': 'LGPL-3',
    'depends': [
        'contacts',
        'sale_management',
        'stock',
        'partner_credit_limit'
        ],
    'data': [
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/ffacsa_webservice_log_views.xml',
        'views/partner_views.xml',
        'views/town_views.xml',
        'views/product_pricelist_views.xml',
        'views/account_views.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/res_users_views.xml',
        'views/stock_views.xml',
        'wizard/import_partner_views.xml',
        'wizard/import_partner_additional_views.xml',
        'wizard/import_product_views.xml',
        
    ],
}