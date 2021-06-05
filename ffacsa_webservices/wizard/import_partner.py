# -*- coding: utf-8 -*-

import logging

from odoo import _, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import GET_DATA

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
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OCRD', orderBy='CardCode', pageSize=100, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER( 'partner', record, record['CardCode'] )
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )

        if self.contacts:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OCPR', orderBy='CntctCode', pageSize=100, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER( 'contact', record, record['CntctCode'] )
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False 
                else:
                    _logger.info( 'No HTTP resource was found' )

        if self.address:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'CRD1', orderBy='CardCode', pageSize=100, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('address', record, '')
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
    