# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    branch_id = fields.Many2one('res.branch', readonly=False)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        check_company=True)

    @api.onchange('wharehouse_id')
    def _onchange_warehouse(self):
        pass