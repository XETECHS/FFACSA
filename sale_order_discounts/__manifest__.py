# -*- coding: utf-8 -*-

{
    'name': 'Sale Discounts -GRUPO ON-',
    'version': '0.1',
    'category': 'sale',
    'summary': "Sale Discounts -GRUPO ON-",
    'description': """Sale Discount -GRUPO ON-""",
    'author': 'Xetechs, S.A.',
    'website': 'https://www.xetechs.com',
    'depends': ['sale', 'sale_management', 'custom_fields_v13'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/mantenimientos_view.xml',
        'views/menu.xml',
        'views/product_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
