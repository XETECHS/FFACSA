# -*- coding: utf-8 -*-

import logging
import json

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import GET_DATA
from odoo.exceptions import ValidationError

_logger = logging.getLogger( __name__ )


class ImportPartnerAdditional(models.TransientModel):
    _name = 'ffacsa.import.partner.additional'
    _description = 'FFACSA Import Partner Additional'

    groups = fields.Boolean(string='Groups?')
    industries = fields.Boolean(string='Industries?')
    territories = fields.Boolean(string='Territories?')
    pricelists = fields.Boolean(string='Pricelists?')
    conditions = fields.Boolean(string='Payment Conditions?')

    def to_do(self):
        LOGGER = self.env['ffacsa.webservice.log'].logger
        if self.groups:
            data = GET_DATA( 'OCRG' )
            if data:
                for record in data:
                    LOGGER('partner_group', record, record['GroupCode'], update=False)
        else:
            _logger.info( 'No HTTP resource was found' )

        if self.industries:
            data = GET_DATA( 'OOND' )
            if data:
                for record in data:
                    LOGGER('industry', record, record['IndCode'], update=False)
        else:
            _logger.info( 'No HTTP resource was found' )

        if self.territories:
            data = GET_DATA( 'OTER' )
            if data:
                for record in data:
                    LOGGER('territory', record, record['territryID'], update=False)
        else:
            _logger.info( 'No HTTP resource was found' )

        if self.pricelists:
            data = GET_DATA( 'OPLN' )
            if data:
                for record in data:
                    LOGGER('pricelist', record, record['ListNum'], update=False)
        else:
            _logger.info( 'No HTTP resource was found' )

        if self.conditions:
            data = GET_DATA( 'OCTG' )
            if data:
                for record in data:
                    LOGGER('paymenterm', record, record['GroupNum'], update=False)
        else:
            _logger.info( 'No HTTP resource was found' )   