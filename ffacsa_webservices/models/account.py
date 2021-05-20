# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'
    _description = 'Account Payment Term'

    code = fields.Char(string='Code')
    ffacsa_days = fields.Integer(string='Days')
    ffacsa_month = fields.Integer(string='Month')
    spot = fields.Boolean(string='Spot?')