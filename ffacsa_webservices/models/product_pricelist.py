# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class Pricelist(models.Model):
    _inherit = "product.pricelist"
    _description = "Pricelist"

    branch = fields.Char(string="Branch")
    source_id = fields.Char(string='Code')
    #level = fields.Char(string='')


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    base_price =  fields.Float('Base Price', digits='Product Price')
    total_price =  fields.Float('Total Price', digits='Product Price')