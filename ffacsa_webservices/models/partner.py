# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'
    
    phone2 = fields.Char()
    source_id = fields.Char(string='Source')
    business_name = fields.Char(string='Business Name')
    balance = fields.Monetary(string='Balance')
    credit_line = fields.Monetary(string='Credit Line')
    u_category = fields.Char(string="Calif")

    UpdateDate = fields.Datetime(string='')
    #partner_type = fields.Char(string='')

    # FFACSA TABLES

class PartnerGroup(models.Model):
    _name = 'ffacsa.partner.group'
    _description = 'Partner Group'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    type = fields.Selection([('C', 'Customers'), ('S', 'Suppliers')], string='Type')
    locked = fields.Boolean(string='Locked')

class PartnerIndustry(models.Model):
    _name = 'ffacsa.industry'
    _description = 'Partner Industry'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')


class PartnerTerritory(models.Model):
    _name = 'ffacsa.territory'
    _description = 'Partner Territory'
    _rec_name = "code"
    
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    
