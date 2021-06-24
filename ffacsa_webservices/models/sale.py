# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import POST_DATA
from odoo.exceptions import UserError

_logger = logging.getLogger( __name__ )

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        check_company=True)
    branch = fields.Char(related="warehouse_id.branch")
    region_id = fields.Many2one('ffacsa.users.region', string='Region', related="user_id.region_id")
    ffacsa_sale_order = fields.Char(string='FFACSA Order', readonly=True, copy=False)
    
    
    comments = fields.Text('Comments')
    delivery_name = fields.Char('Delivery Name')
    delivery_pdi = fields.Char('Delivery DPI')
    delivery_phone = fields.Char('Telefono Entrega')


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.send_ffacsa_quotation()
        return res



    def send_ffacsa_quotation(self):
        lines = []
        partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
        if partner.street:
            address = partner.street
        else:
            UserError( _("%s hasn't address"% partner))
        if partner.street2:
            address+= partner.street2
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
            'NumAtCard': self.name,
            'CardCode': self.warehouse_id.branch,
            'CardName': self.warehouse_id.name,
            'CodBodega': self.warehouse_id.code,
            'ListNum': int(self.pricelist_id.source_id),
            'FacNIT': partner.vat,
            'FacNom': partner.name,
            'Telefono': partner.phone,
            'EMail': partner.email,
            'EntregaLocal': "2",
            'DireccionEntrega': address,
            'Departamento': int( partner.state_id.code),
            'Municipio': partner.town_id.code,
            'Comments': self.comments,
            'NombreEntrega': self.delivery_name,
            'DPIEntrega': self.delivery_pdi,
            'TelefonoEntrega': self.delivery_phone,
            'DocTotal': self.amount_total,
            'Saldo': self.amount_total,
            'Detalle': lines,
        }

        _logger.info( quotation )
        data = POST_DATA( quotation )
        if data.get('DocNum'):
            self.ffacsa_sale_order = data.get('DocNum')
        else:
            raise UserError(_( data ))