# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class Pricelist(models.Model):
    _inherit = "product.pricelist"
    _description = "Pricelist"

    # @api.model
    # def _allowed_branches(self):
    #     a = self.env.user.branch_ids.ids
    #     return [('id', 'in', self.env.user.branch_ids.ids)]

    # branch_id = fields.Many2one('res.branch', string="Branch", domain=_allowed_branches)
    code = fields.Char(string='Code')
    #level = fields.Char(string='')


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    base_price =  fields.Float('Base Price', digits='Product Price')
    total_price =  fields.Float('Total Price', digits='Product Price')