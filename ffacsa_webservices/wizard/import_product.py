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
    subcateg = fields.Boolean(string='subCategories?')

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
        if self.group:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OITB', orderBy='ItmsGrpCod', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('product_group', record, record['ItmsGrpCod'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False
        
        if self.price:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'ITM1', orderBy='ItemCode', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('price', record, record['ItemCode'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False

        if self.inventory:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OITW', orderBy='ItemCode', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('inventory', record, record['ItemCode'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False

        if self.warehouse:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'OWHS', orderBy='WhsCode', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('warehouse', record, record['WhsCode'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False
        
        if self.categ:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'ItemCategoria', orderBy='Code', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('categ', record, record['Code'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False
        if self.subcateg:
            end, pageNumber = True, 1
            while end:
                data = GET_DATA( 'ItemSubCategoria', orderBy='Code', pageSize=50, pageNumber=pageNumber )
                if data:
                    for record in data['Results']:
                        LOGGER('subcateg', record, record['Code'])
                    if data['NextPageUrl']:
                        pageNumber+=1
                    else:
                        end = False
                else:
                    _logger.info( 'No HTTP resource was found' )
                    end = False