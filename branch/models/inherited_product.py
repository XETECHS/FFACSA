# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTemplateIn(models.Model):
    _inherit = 'product.template'

    
    @api.model
    def default_get(self, default_fields):
        res = super(ProductTemplateIn, self).default_get(default_fields)
        if self.env.user.branch_id:
            res.update({
                'branch_id' : self.env.user.branch_id.id or False
            })
        return res

    @api.model
    def _allowed_branches(self):
        a = self.env.user.branch_ids.ids
        return [('id', 'in', self.env.user.branch_ids.ids)]

    branch_id = fields.Many2one('res.branch', string="Branch", domain=_allowed_branches)