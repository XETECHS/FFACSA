# -*- coding: utf-8 -*-

import requests

URL = 'http://portal.ffacsa.com/desktopmodules/ffacsaAppsCRM/API/SAPData/GetSAPData'
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
    'OWHS' :'owhs'
}

def GET_DATA(table=False):
    if not table:
        return False
    payload = {'tableName': TABLES[table]}
    response = requests.get(URL, params=payload)
    if response.status_code == requests.codes.ok:
        return response.json()
    return False