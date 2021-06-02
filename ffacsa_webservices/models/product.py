# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'
    
    code = fields.Char(string='Code', required=True)