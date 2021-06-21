# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import GET_DATA

_logger = logging.getLogger( __name__ )

class ffacsaTown(models.Model):
    _name = 'ffacsa.town'
    _description = 'Ffacsa Town'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Integer(string='Code', readonly=True)
    state_id = fields.Many2one('res.country.state', string='State')

    def action_import(self):
        state = self.env['res.country.state']
        data = GET_DATA( 'MUNICIPIOS' )
        if data:
            for record in data:
                state_id = state.search( [('code', '=', record.get('COD_DEPTO'))], limit=1)
                self.create({
                    'name': record.get('DESC_MUNIC'),
                    'code': record.get('COD_MUNIC'),
                    'state_id': state_id.id if state_id else False
                })
        else:
            _logger.info( 'No HTTP resource was found' )