# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('wharehouse_id')
    def _onchange_warehouse(self):
        self.branch_id = self.warehouse_id.branch_id

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.env.user.branch_ids:
            warehouse_id = self.env['stock.warehouse'].search(([('branch_id', 'in', self.env.user.branch_ids.ids)]))
            if len(warehouse_id):
                self.warehouse_id = warehouse_id[0]
                self.branch_id = self.warehouse_id.branch_id
        elif self.company_id:
            warehouse_id = self.env['ir.default'].get_model_defaults('sale.order').get('warehouse_id')
            self.warehouse_id = warehouse_id or self.env['stock.warehouse'].search(
                [('company_id', '=', self.company_id.id)], limit=1)
            print(self.warehouse_id)

    @api.model
    def _allowed_warehouse(self):
        warehouse = self.env['stock.warehouse'].search(([('branch_id', 'in', self.env.user.branch_ids.ids)]))
        return [('id', 'in', warehouse.ids)]


    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['branch_id'] = self.branch_id.id
        return res

    branch_id = fields.Many2one('res.branch', related='warehouse_id.branch_id', readonly=True)

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Almacen',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        check_company=True, domain=_allowed_warehouse, default=False)





SaleOrder()