# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    country_id = fields.Many2one( default= lambda s: s.env.ref('base.gt') )
    town_id = fields.Many2one('ffacsa.town', string="Town")
    # CONTACT INFORMATION
    first_name  = fields.Char(string='First Name', readonly=True)
    middle_name = fields.Char(string='Middle Name', readonly=True)
    last_name = fields.Char(string='Last Name', readonly=True)

    ffacsa_group_id = fields.Many2one('ffacsa.partner.group', string='FFACSA Group', readonly=True)
    ffacsa_industry_id = fields.Many2one('ffacsa.industry', string='FFACSA Industry', readonly=True)
    ffacsa_territory_id = fields.Many2one('ffacsa.territory', string='FFACSA Territory', readonly=True)

    phone = fields.Char(size=20)
    phone2 = fields.Char(size=20)
    source_id = fields.Char(string='Source', readonly=True)
    business_name = fields.Char(string='Business Name', readonly=True)
    balance = fields.Monetary(string='Balance', readonly=True)
    u_category = fields.Char(string="Calif", readonly=True)

    #UpdateDate = fields.Datetime(string='')
    #credit_line = fields.Monetary(string='Credit Line')
    SlpCode = fields.Char(string='Seller Code', readonly=True)
    portalURL = fields.Char(string='portal URL', readonly=True)
    
    def go_portalURL(self):
        if self.portalURL:
            return {
                "type": "ir.actions.act_url",
                "url": self.portalURL,
                "target": "new",
            }    

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
    
