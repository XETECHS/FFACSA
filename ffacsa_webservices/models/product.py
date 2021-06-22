# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'
    

    default_code = fields.Char(readonly=True)
    service_to_purchase = fields.Boolean("Purchase Automatically", help="If ticked, each time you sell this product through a SO, a RfQ is automatically created to buy the product." 
                "Tip: don't forget to set a vendor on the product.")
    portalURL = fields.Char(string='portal URL', readonly=True)


    def go_portalURL(self):
        if self.portalURL:
            return {
                "type": "ir.actions.act_url",
                "url": self.portalURL,
                "target": "new",
            } 

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product'
    
    default_code = fields.Char(readonly=True)
    service_to_purchase = fields.Boolean("Purchase Automatically", help="If ticked, each time you sell this product through a SO, a RfQ is automatically created to buy the product." 
                "Tip: don't forget to set a vendor on the product.")
    portalURL = fields.Char(string='portal URL', readonly=True)


    def go_portalURL(self):
        if self.portalURL:
            return {
                "type": "ir.actions.act_url",
                "url": self.portalURL,
                "target": "new",
            } 


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code = fields.Char(string="Code", readonly=True)

class ProductGroup(models.Model):
    _name = 'ffacsa.product.group'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')