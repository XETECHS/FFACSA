# -*- coding: utf-8 -*-

import json
from datetime import datetime

from odoo import _, api, fields, models

TYPE = [
    ('partner', 'Partner'),
    ('contact', 'Contacts'),
    ('address', 'Address'),
    ('partner_group', 'Partner Group'),
    ('industry', 'Industry'),
    ('territory', 'Territory'),
    ('pricelist', 'Pricelist'),
    ('paymenterm', 'Payment Term'),

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
            try:
                data = json.loads( record.data )
                if record.operation == 'create':
                    self._create_record(data=data, type=record.type)
                    
                else:
                    self._update_record(data=data, type=record.type)
                record.write({'state': 'done'})
            except:
                record.write({'state': 'fail'})

    def logger(self, type, data, id, update=False):
        values = {
                'type': type,
                'source_id': id,
                'data': json.dumps( data ),
                'operation': 'update' if update else 'create'
            }
        self.create( values )
        self.env.cr.commit()
        return

    def _create_record(self ,data=False, type=False):
        partner = self.env['res.partner']
        if not data or not type:
            return
        if type == 'partner':
            partner.create({
                'type': 'contact',
                'company_type': 'company',
                'name': data.get('CardName', ''),
                'vat': data.get('AddId', ''),
                'phone': data.get('Phone1', ''),
                'phone2': data.get('Phone2', ''),
                'mobile': data.get('Cellular', ''),
                'email': data.get('E_Mail', ''),
                'source_id': data.get('CardCode', ''),
                'business_name': data.get('CardFName', ''),
                'balance': data.get('Balance', 0.0),
                'credit_line': data.get('CreditLine', 0.0),
                'u_category': data.get('', ''),
                #'UpdateDate': data.get('', ''),
            })
        elif type == 'contact':
            parent_id = partner.search([('source_id', '=', data.get('CardCode') )])
            comment = ''
            if data.get('Notes1'):
                comment = data.get('Notes1')
            if data.get('Notes2'):
                comment+=data.get('Notes2')
            partner.create({
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
            })
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
            self.env['ffacsa.partner.group'].create({
                'code': data.get('GroupCode', ''),
                'name': data.get('GroupName', ''),
                'type': data.get('GroupType', ''),
                'locked': False if data.get('Locked') == 'N' else True
            })
        elif type=='industry':
            self.env['ffacsa.industry'].create({
                'code': data.get('IndCode', ''),
                'name': data.get('IndName', ''),
                'description': data.get('IndDesc', ''),
            })
        elif type=='territory':
            self.env['ffacsa.territory'].create({
                'code': data.get('territryID', ''),
                'description': data.get('descript', ''),
            })
        elif type=='pricelist':
            self.env['product.pricelist'].create({
                'code': data.get('ListNum', ''),
                'name': data.get('ListName', ''),
                'active': True if data.get('ValidFor', '') == 'Y' else False,
                # 'branch_id': data.get('U_Agencia', ''),
                # 'level': data.get('U_Nivel', ''),
            })
        elif type=='paymenterm':
            self.env['account.payment.term'].create({
                'code': str( data.get('GroupNum', '') ),
                'name': data.get('PymntGroup', ''),
                'ffacsa_month': data.get('ExtraMonth', '') ,
                'ffacsa_days': data.get('ExtraDays', ''),
                'spot': True if data.get('Contado', '') == 'Y' else False,
            })
        else:
            return