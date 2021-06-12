# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    special_service = fields.Boolean('Servicio especial', required=False, default=False)

ProductTemplate()
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount = fields.Float('Descuento', compute="_compute_global_discount", store=False)
    amount_total_without_special = fields.Float('Total sin especial', compute="_compute_total_without_special", store=False)
    new_order = fields.Boolean('New')
    #new fields
    apply_manual_discount = fields.Boolean('Descuento manual', default=False)
    manual_discount = fields.Float('Descuento (%)', default=0.00)

    @api.depends('new_order', 'order_line.product_uom_qty', 'order_line.price_unit')
    def _compute_total_without_special(self):
        """
        Compute the total amounts without special service.
        """
        for order in self:
            amount_total = 0.0
            for line in order.order_line:
                if line.product_id.special_service != True and order.new_order == True:
                    amount_total += (line.product_uom_qty * line.price_unit)
            order.update({
                'amount_total_without_special': amount_total or 0.00,
            })

    @api.depends('amount_total_without_special', 'company_id', 'apply_manual_discount', 'manual_discount')
    def _compute_global_discount(self):
        discount_obj = self.env['on.mantenimiento']
        discount = 0.00
        for rec in self:
            discount_obj = self.env['on.mantenimiento']
            discount = 0.00
            if rec.amount_total > 0.00 and rec.new_order == True:
                if rec.apply_manual_discount == True:
                    discount = rec.manual_discount
                else:
                    discount_ids = discount_obj.search([('company_id', '=', rec.company_id.id)])
                    for item in discount_ids:
                        if item.rango_inferior <= rec.amount_total_without_special <= item.rango_superior:
                            discount = item.porcentaje_descuento
            rec.update({
                'global_discount': discount or 0.00,
            })


    @api.model
    def default_get(self, default_fields):
        values = super(SaleOrder, self).default_get(default_fields)
        values['new_order'] = True
        return values

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        for rec in res:
            for line in rec.order_line:
                if rec.global_discount > 0.00 and line.product_id.special_service == False: 
                    line.discount = rec.global_discount or 0.00
        return res


SaleOrder()

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    global_discount = fields.Float('Descuento', related="order_id.global_discount", store=False)
    #discount = fields.Float(string='Discount (%)', digits='Discount', related="order_id.global_discount")
    discount = fields.Float(string='Discount (%)', digits='Discount', compute="_compute_discount_per_line")
    global_discount_amount = fields.Float('Monto Descuento', compute="_compute_line_global_discount", store=False)
    edit_price = fields.Boolean('Editar precio', compute="_compute_edit_price")


    @api.depends('product_id', 'order_id.global_discount')
    def _compute_discount_per_line(self):
        for line in self:
            discount = 0.00
            if line.product_id and line.product_id.special_service == False:
                discount = line.order_id.global_discount
            line.update({
                'discount': discount,
            })

    @api.depends('product_id')
    def _compute_edit_price(self):
        for line in self:
            edit_price = False
            if self.env.user.has_group('base.group_system'):
                edit_price = True
            if self.env.user.has_group('sale_order_discounts.group_write_price_unit'):
                if line.product_id and line.product_id.special_service == True:
                    edit_price = True
            line.update({
                'edit_price': edit_price,
            })


    @api.depends('product_id', 'price_unit', 'product_uom_qty', 'global_discount')
    def _compute_line_global_discount(self):
        discount = 0.00
        for line in self:
            discount = 0.00
            if line.global_discount and line.product_id.special_service == False: 
                discount = (line.price_unit * (line.global_discount / 100))
            line.update({
                'global_discount_amount': (line.product_uom_qty  * discount),
            })

    #@api.onchange('global_discount', 'product_id', 'global_discount_amount', 'price_unit', 'product_uom_qty')
    #def _onchange_global_discount(self):
    #    #Onchange discount
    #    self.discount = 0.00
    #    if not (self.product_id and self.global_discount and self.product_uom_qty and self.global_discount_amount and self.price_unit):
    #        return
    #    if self.global_discount:
    #        if self.product_id.special_service != True and self.global_discount > 0.00:
    #            self.discount = 0.00
    #            self.discount = self.global_discount
    #        else:
    #            self.discount = 0.00
    #    else:
    #        self.discount = 0.00

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'global_discount', 'global_discount_amount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = 0.00
            if line.global_discount:
                if line.product_id.special_service == False:
                    price = line.price_unit * (1 - (line.global_discount or 0.0) / 100.0)
                else:
                    price = line.price_unit
            else:
                if line.product_id.special_service == False:
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                else:
                    price = line.price_unit
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': (taxes['total_included']),
                'price_subtotal': (taxes['total_excluded']),
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    #@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'global_discount_amount')
    #def _compute_amount(self):
    #    res = super(SaleOrderLine, self)._compute_amount()
    #    for line in self:
    #        subtotal = line.price_subtotal
    #        line.update({
    #            'price_subtotal': (subtotal - line.global_discount_amount) or 0.00,
    #        })
    #    return res

    #def _prepare_invoice_line(self):
    #    res = super(SaleOrderLine, self)._prepare_invoice_line()
    #    for line in self:
    #        if line.product_id.special_service == False:
    #            res.update({
    #                'discount': line.global_discount or 0.00,
    #            })
    #    return res

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount if self.product_id.special_service == False else 0.00,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res

SaleOrderLine() 