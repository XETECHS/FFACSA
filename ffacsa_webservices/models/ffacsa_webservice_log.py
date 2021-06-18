# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from odoo import _, api, fields, models
_logger = logging.getLogger( __name__ )

TYPE = [
    ('partner', 'Partner'),
    ('contact', 'Contacts'),
    ('address', 'Address'),
    ('partner_group', 'Partner Group'),
    ('industry', 'Industry'),
    ('territory', 'Territory'),
    ('pricelist', 'Pricelist'),
    ('paymenterm', 'Payment Term'),
    ('product', 'Product'),
    ('price', 'Price'),
    ('inventory', 'Inventory'),
    ('product_group', 'Product Group'),
    ('warehouse', 'Warehouse'),
    ('categ', 'Category'),
    ('subcateg', 'SubCategory'),
]


class WebserviceLog(models.Model):
    _name = 'ffacsa.webservice.log'
    _description = 'FFACSA Webservice Log'

    #LOG FIELDS
    date = fields.Datetime(string="Date", default=datetime.now())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('fail', 'Fail'),
        ('done', 'Done'),
    ], string='State', default="draft")
    type = fields.Selection(TYPE, string='Type')
    operation =  fields.Selection([
        ('create', 'Create'),
        ('update', 'Update'),], string="Operation ")

    # RESPONSE DATA
    source_id = fields.Char(string='Source ID')
    data = fields.Text(string='Data')

    def action_process(self):
        for record in self:
            #try:
            data = json.loads( record.data )
            self._create_record(data=data, type=record.type)
            record.write({'state': 'done'})
            #except:
            #record.write({'state': 'fail'})

    def logger(self, type, data, id):
        values = {
                'type': type,
                'source_id': id,
                'data': json.dumps( data ),
                'operation': 'create'
            }
        self.create( values )
        self.env.cr.commit()
        return

    def _create_record(self ,data=False, type=False):
        partner = self.env['res.partner']
        if not data or not type:
            return
        if type == 'partner':
            partner_id = partner.search([('source_id', '=', data.get('CardCode') )], limit=1)
            group_id = self.env['ffacsa.partner.group'].search( [('code', '=', data.get('GroupCode', ''))], limit=1 )
            industry_id = self.env['ffacsa.industry'].search( [('code', '=', data.get('IndustryC', ''))], limit=1 )
            territory_id = self.env['ffacsa.territory'].search( [('code', '=', data.get('Territory', ''))], limit=1 )
            payment_term_id = self.env['account.payment.term'].search( [('code', '=', data.get('GroupNum', ''))], limit=1 )
            product_pricelist = self.env['product.pricelist'].search( [('code', '=', data.get('ListNum', ''))], limit=1 )
            values = {
                    'type': 'contact',
                    'company_type': 'company',
                    'name': data.get('CardName', ''),
                    'vat': data.get('AddId', ''),
                    'ffacsa_group_id': group_id.id,
                    'ffacsa_industry_id': industry_id.id,
                    'ffacsa_territory_id': territory_id.id,
                    'property_payment_term_id': payment_term_id.id,
                    'property_product_pricelist': product_pricelist.id,
                    'phone': data.get('Phone1', ''),
                    'phone2': data.get('Phone2', ''),
                    'mobile': data.get('Cellular', ''),
                    'email': data.get('E_Mail', ''),
                    'source_id': data.get('CardCode', ''),
                    'business_name': data.get('CardFName', ''),
                    'website': data.get('IntrntSite', ''),
                    'balance': data.get('Balance', 0.0),
                    'over_credit': data.get('CreditLine', 0.0),
                    'u_category': data.get('', ''),
                    #'UpdateDate': data.get('', ''),
                }
            if not partner_id:
                partner.create( values )
                _logger.info( 'Create Partner' )
            else:
                self._update_record(values, 'res.partner', partner_id.id)
                _logger.info( values )
            
        elif type == 'contact':
            partner_id = partner.search([('source_id', '=', data.get('CntctCode') )], limit=1)
            parent_id = partner.search([('source_id', '=', data.get('CardCode') )])
            comment = ''
            if data.get('Notes1'):
                comment = data.get('Notes1')
            if data.get('Notes2'):
                comment+=data.get('Notes2')
            values = {
                'type': 'contact',
                'parent_id': parent_id.id if parent_id else False,
                'street': data.get('Address', ''),
                'name': data.get('Name', ''),
                'function': data.get('Position', ''),
                'phone': data.get('Tel1', ''),
                'phone2': data.get('Tel2', ''),
                'mobile': data.get('Cellolar', ''),
                'email': data.get('E_MailL', ''),
                'source_id': data.get('CntctCode', ''),
                'first_name': data.get('FirstName', ''),
                'middle_name': data.get('MiddleName', ''),
                'last_name': data.get('LastName', ''),
                'comment': comment,
                #'UpdateDate': data.get('', ''),
            }
            if not partner_id:   
                partner.create( values )
            else:
                self._update_record(values, 'res.partner', partner_id.id)
        elif type == 'address':
            parent_id = partner.search([('source_id', '=', data.get('CardCode') )])
            country_id = self.env['res.country'].search([('code', '=', data.get('County')) ])
            if not country_id:
                country_id = self.env.ref('base.gt')

            
            partner.create({
                'type': 'invoice' if data.get('CardName', '') == 'B' else 'delivery',
                #'company_type': 'company',
                'name': data.get('Address'),
                'parent_id': parent_id.id if parent_id else False,
                'street': data.get('Address', ''),
                'vat': data.get('TaxOffice', ''),
                #'phone': data.get('LineNum', ''),
                'street': data.get('Address2'),
                'street2': data.get('Address3'),
                'country_id': country_id.id
                #'UpdateDate': data.get('', ''),
            })
        
        elif type== 'partner_group':
            group = self.env['ffacsa.partner.group']
            group_id = group.search( [('code', '=', 'GroupCode')], limit=1 )
            values = {
                    'code': data.get('GroupCode', ''),
                    'name': data.get('GroupName', ''),
                    'type': data.get('GroupType', ''),
                    'locked': False if data.get('Locked') == 'N' else True
                }
            if not group_id:
                group.create( values )
            else:
                self._update_record( values )
        elif type=='industry':
            industry = self.env['ffacsa.industry']
            industry_id = industry.search( [('code', '=', 'IndCode')], limit=1 )
            values = {
                    'code': data.get('IndCode', ''),
                    'name': data.get('IndName', ''),
                    'description': data.get('IndDesc', ''),
                }
            if not industry_id:
                industry.create( values )
            else:
                self._update_record( values , 'ffacsa.industry', industry_id.id)
        elif type=='territory':
            territory = self.env['ffacsa.territory']
            territory_id = territory.search( [('code', '=', 'territryID')], limit=1 )
            values = {
                    'code': data.get('territryID', ''),
                    'description': data.get('descript', ''),
                }
            if not territory_id:
                territory.create( values )
            else:
                self._update_record( values , 'ffacsa.territory', territory_id.id)
        elif type=='pricelist':
            pricelist = self.env['product.pricelist']
            pricelist_id = pricelist.search([('code', '=', 'ListNum')], limit=1)
            values = {
                'code': data.get('ListNum', ''),
                'name': data.get('ListName', ''),
                'active': True if data.get('ValidFor', '') == 'Y' else False,
                # 'branch_id': data.get('U_Agencia', ''),
                # 'level': data.get('U_Nivel', ''),
            }
            if not pricelist_id:
                pricelist.create( values )
            else:
                self._update_record(values, 'product.pricelist', pricelist_id.id)
        elif type=='paymenterm':
            payment_term = self.env['account.payment.term']
            payment_term_id = payment_term.search( [('code', '=', 'GroupNum')], limit=1 )
            values = {
                'code': str( data.get('GroupNum', '') ),
                'name': data.get('PymntGroup', ''),
                'ffacsa_month': data.get('ExtraMonth', '') ,
                'ffacsa_days': data.get('ExtraDays', ''),
                'spot': True if data.get('Contado', '') == 'Y' else False,
            }
            if not payment_term_id:
                payment_term.create( values )
            else:
                self._update_record(values, 'account.payment.term', payment_term_id.id)
        
        elif type=='product':
            product = self.env['product.product']
            product_id = product.search( [('code', '=',  data.get('ItemCode', '') )], limit=1 )
            values = {
                'code': str( data.get('ItemCode', '') ),
                'name': data.get('ItemName', ''),
                'default_code': data.get('ItemCode', ''),
                'description_sale': data.get('FrgnName', ''),
                'type': 'product',
                'sale_ok': data.get('SellItem', '') == 'Y',
                'purchase_ok': data.get('PrchseItem', '') == 'Y',
                'volume': data.get('SVolume', ''),
                'weight': data.get('SWeight1', ''),
                'description': data.get('UserText', ''),
                #'categ_id': ItemCategoria,
                #'website_published': data.get('PublicarWeb', '') == 'Y',
            }
            _logger.info( values )
            if not product_id:
                product.create( values )
            else:
                self._update_record(values, 'product.product', product_id.id)
        
        elif type=="price":
            product_id = self.env['product.product'].search(
                [('code', '=', data.get('ItemCode', ''))]
            )
            pricelist_id = self.env['product.pricelist'].search(
                [('code', '=', data.get('ListNum', ''))]
            )

            values = {
                'product_tmpl_id': product_id.product_tmpl_id.id,
                'pricelist_id': pricelist_id.id,
                'date_start':  data.get('FromDate', ''),
                'date_end': data.get('ToDate', ''),
                'fixed_price': data.get('Price', ''),
                'base_price': data.get('BasePrice', ''),
                'total_price': data.get('PriceAfVAT', ''),
            }
            self.env['product.pricelist.item'].create( values )
        elif type=="inventory":
            #product_group = self.env['ffacsa.product.group']
            pass
        
        elif type=='product_group':
            product_group = self.env['ffacsa.product.group']
            product_group_id = product_group.search( [('code', '=', data.get('ItmsGrpCod', ''))], limit=1)
            values = {
                'name': data.get('ItmsGrpNam', ''),
                'code': data.get('ItmsGrpCod', ''),
            }
            if not product_group_id:
                product_group.create( values )
            else:
                self._update_record(values, 'ffacsa.product.group', product_group_id.id)
        elif type=='warehouse':
            warehouse = self.env['stock.warehouse']
            warehouse_id = warehouse.search( [('code', '=', data.get('WhsCode', ''))], limit=1)
            values = {
                'code': data.get('WhsCode', ''),
                'name': data.get('WhsName', ''),
                #'Agencia': data.get('Agencia', ''),
            }
            if not warehouse_id:
                warehouse_id.create( values )
            else:
                self._update_record(values, 'stock.warehouse', warehouse_id.id)
        
        elif type=='categ':
            categ = self.env['product.category']
            categ_id = categ.search( [('code', '=', data.get('Code', ''))], limit=1)
            values = {
                'code': data.get('Code', ''),
                'name': data.get('Name', ''),
            }
            if not categ_id:
                categ_id.create( values )
            else:
                self._update_record(values, 'product.category', categ_id.id)
        elif type=='subcateg':
            categ = self.env['product.category']
            categ_id = categ.search( [('code', '=', data.get('Code', ''))], limit=1)
            values = {
                'code': data.get('Code', ''),
                'name': data.get('Name', ''),
            }
            if not categ_id:
                parent_id = categ.search( [('name', '=', data.get('Categoria', ''))], limit=1)
                values['parent_id'] = parent_id.id if parent_id else False
                categ_id.create( values )
            else:
                self._update_record(values, 'product.category', categ_id.id)
        else:
            return

    def _update_record(self, values, object, id):
        _logger.info( [object, id] )
        record = self.env[object].browse( id )
        record.write(
            values
        )