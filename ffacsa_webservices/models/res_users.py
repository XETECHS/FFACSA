from odoo import _, api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Res Users'
    
    code_sap = fields.Char(string='SAP ID')
    region_id = fields.Many2one('ffacsa.users.region', string='Region')


class ffacsaUsersRegion(models.Model):
    _name = 'ffacsa.users.region'
    _description = 'ffacsa Users Region'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')