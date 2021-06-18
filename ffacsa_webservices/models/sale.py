# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import POST_DATA

_logger = logging.getLogger( __name__ )

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    branch_id = fields.Many2one('res.branch', readonly=False)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        check_company=True)
    region_id = fields.Many2one('ffacsa.users.region', string='Region', related="user_id.region_id")

    @api.onchange('wharehouse_id')
    def _onchange_warehouse(self):
        pass

    def send_ffacsa_quotation(self):
        lines = []
        i=1
        for line in self.order_line:
            lines.append( {
                'LineNum' : i,
                'ItemCode' : line.product_id.code,
                'Dscription': line.name,
                'Quantity': line.product_uom_qty,
                'Price': line.price_unit,
                'LineTotal' : line.price_total,
                'GTotal' : line.price_total,
                'TotalRecargo' : 0.0
            }) 
            i=i+1
        quotation = {
            'DocDate': self.date_order.strftime('%Y-%m-%dT%H:%M:%S'),
            'DocStatus': 'O',
            'CardCode': self.partner_id.source_id,
            'CardName': self.partner_id.name,
            'FacNIT': self.partner_id.vat,
            'FacNom': self.partner_id.name,
            'Telefono': self.partner_id.phone,
            'EMail': self.partner_id.email,
            'EntregaLocal': "2",
            'DireccionEntrega': self.partner_id.street or '' + self.partner_id.street2 or '',
            'Departamento': 1,
            'Municipio': 113,
            'Comments': self.partner_id.street or '' + self.partner_id.street2 or '',
            'NombreEntrega': self.partner_id.name,
            'DPIEntrega': 0,
            'TelefonoEntrega': False,
            'DocTotal': self.amount_total,
            'Saldo': self.amount_total,
            'Detalle': lines
        }
        _logger.info( quotation )
        data = POST_DATA(quotation)

        return data