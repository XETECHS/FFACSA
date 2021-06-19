
# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Stock Warehouse'

    branch = fields.Char(string='Branch', readonly=True)
    region_id = fields.Many2one('ffacsa.users.region', string='Region')
