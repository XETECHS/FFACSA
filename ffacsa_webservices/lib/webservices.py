# -*- coding: utf-8 -*-

import requests
import logging
import json

from odoo.exceptions import UserError

_logger = logging.getLogger( __name__ )

URL = 'http://portal.ffacsa.com/desktopmodules/ffacsaAppsCRM/API/SAPData/GetSAPData'
URL_ORDER = 'http://portal.ffacsa.com/API/ffacsaAppsCotiCRM/Cotizacion/SaveQuote'

TABLES = {
    # PARTNERS
    'OCRD': 'ocrd',
    'OCPR': 'ocpr',
    'CRD1': 'crd1',
    # PARTNER GROUPS
    'OCRG': 'ocrg',
    # INDUSTRIES
    'OOND': 'oond',
    # TERRIORIES
    'OTER': 'oter',
    # PRICE LIST
    'OPLN': 'opln',
    # Payment Conditions
    'OCTG': 'octg',

    # PRODUCT
    'OITM': 'oitm',
    # PRICE 
    'ITM1': 'itm1',
    # INVENTORY
    'OITW': 'oitw',
    # PRODUCT GROUPS 
    'OITB': 'oitb',
    # WAREHOUSE
    'OWHS' :'owhs',
    # PRODUCT CATEG
    'ItemCategoria': 'ItemCategoria',
    #PRODUCT SUBCATEG
    'ItemSubCategoria': 'ItemSubCategoria',
}


def GET_DATA(table, **kwargs):
    payload = {'tableName': TABLES[table]}
    if kwargs:
        payload.update( kwargs )
    response = requests.get(URL, params=payload)
    _logger.info( 'REQUESTS FOR: %s FOR PAGE: %s'%(TABLES[table], payload.get('pageNumber', 1)) )
    if response.status_code == requests.codes.ok:
        return response.json()
    return False

def POST_DATA(quotation, **kwargs):
    payload = quotation
    if kwargs:
        payload.update( kwargs )
    response = requests.post(URL_ORDER, json=payload)
    _logger.info( response.json() )
    if response.status_code == requests.codes.ok:
        return response.json()
    return False