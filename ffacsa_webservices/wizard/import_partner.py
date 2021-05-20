# -*- coding: utf-8 -*-

import logging
import json

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import GET_DATA
from odoo.exceptions import ValidationError

_logger = logging.getLogger( __name__ )


class ImportPartner(models.TransientModel):
    _name = 'ffacsa.import.partner'
    _description = 'FFACSA Import Partner'

    partners = fields.Boolean(string='Partners?')
    contacts = fields.Boolean(string='Contacts?')
    address = fields.Boolean(string='Address?')

    def to_do(self):
        LOGGER = self.env['ffacsa.webservice.log'].logger
        if self.partners:
            data = GET_DATA( 'OCRD' )
            count = 10
            if data:
                #for record in data:
                for record in data:
                    if count:
                        LOGGER('partner', record, record['CardCode'], update=False)
                        count-=1
                    else: 
                        continue
            else:
                _logger.info( 'No HTTP resource was found' )

        if self.contacts:
            data = GET_DATA( 'OCPR' )
            count = 10
            if data:
                #for record in data:
                for record in data:
                    if count:
                        #_logger.info( record )
                        LOGGER('contact', record, record['CntctCode'], update=False)
                        count-=1
                    else: 
                        continue
            else:
                _logger.info( 'No HTTP resource was found' )

        if self.address:
            data = GET_DATA( 'CRD1' )
            count = 10
            if data:
                #for record in data:
                for record in data:
                    if count:
                        #_logger.info( record )
                        LOGGER('address', record, '', update=False)
                        count-=1
                    else: 
                        continue
        else:
            _logger.info( 'No HTTP resource was found' )
    