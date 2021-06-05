# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.addons.ffacsa_webservices.lib.webservices import GET_DATA
from odoo.exceptions import ValidationError

_logger = logging.getLogger( __name__ )


class ImportProduct(models.TransientModel):
    _name = 'ffacsa.import.product'
    _description = 'FFACSA Import Product'

    product = fields.Boolean(string='Product?')
    price = fields.Boolean(string='Price?')
    inventory = fields.Boolean(string='Adjustment Inventory?')
    group = fields.Boolean(string='Groups?')
    warehouse = fields.Boolean(string='Warehouses?')
    categ = fields.Boolean(string='Categories?')

    def to_do(self):
        LOGGER = self.env['ffacsa.webservice.log'].logger
        if self.product:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OITM', orderBy='ItemCode', pageSize=100, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('product', record, record['ItemCode'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False