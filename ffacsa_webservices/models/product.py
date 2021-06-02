# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'
    
    code = fields.Char(string='Code')
    service_to_purchase = fields.Boolean("Purchase Automatically", help="If ticked, each time you sell this product through a SO, a RfQ is automatically created to buy the product." 
                "Tip: don't forget to set a vendor on the product.")