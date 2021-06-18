
# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Stock Warehouse'

    code = fields.Char(string='Code')
    region_id = fields.Many2one('ffacsa.users.region', string='Region')
