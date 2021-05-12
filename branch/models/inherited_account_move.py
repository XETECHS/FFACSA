# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare




class AccountMove(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        previous_journal = self.journal_id.id
        res = super(AccountMove, self).write(vals)
        if previous_journal != self.journal_id.id and self.company_id.id == 4 and self.journal_id.type == 'sale':
            for line in self.invoice_line_ids:
                line.account_id = self.journal_id.default_credit_account_id.id
        return res

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMove, self).default_get(default_fields)
        branch_id = False
        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id': branch_id
        })
        return res

    @api.model
    def _allowed_branches(self):
        a = self.env.user.branch_ids.ids
        return [('id', 'in', self.env.user.branch_ids.ids)]

    @api.model
    def _get_default_journal(self):
        ''' Get the default journal.
        It could either be passed through the context using the 'default_journal_id' key containing its id,
        either be determined by the default type.
        '''
        move_type = self._context.get('default_type', 'entry')
        journal_type = 'general'
        if move_type in self.get_sale_types(include_receipts=True):
            journal_type = 'sale'
        elif move_type in self.get_purchase_types(include_receipts=True):
            journal_type = 'purchase'

        if self._context.get('default_journal_id'):
            journal = self.env['account.journal'].browse(self._context['default_journal_id'])

            if move_type != 'entry' and journal.type != journal_type:
                raise UserError(_("Cannot create an invoice of type %s with a journal having %s as type.") % (
                move_type, journal.type))

        else:
            company_id = self._context.get('force_company',
                                           self._context.get('default_company_id', self.env.company.id))
            domain = [('company_id', '=', company_id), ('type', '=', journal_type)]

            if company_id == 4 and journal_type == 'sale':
                domain = domain + [('branch_id', 'in', self.env.user.branch_ids.ids)]


            journal = None
            if self._context.get('default_currency_id'):
                currency_domain = domain + [('currency_id', '=', self._context['default_currency_id'])]
                journal = self.env['account.journal'].search(currency_domain, limit=1)

            if not journal:
                journal = self.env['account.journal'].search(domain, limit=1)

            if not journal:
                error_msg = _('Please define an accounting miscellaneous journal in your company')
                if journal_type == 'sale':
                    error_msg = _('Please define an accounting sale journal in your company')
                elif journal_type == 'purchase':
                    error_msg = _('Please define an accounting purchase journal in your company')
                raise UserError(error_msg)
        return journal

    @api.model
    def _journal_branch_domain(self):
        invoice_type = self._context.get('default_type')
        journal_type = []
        if invoice_type == 'out_invoice' or invoice_type == 'out_refund' or invoice_type == 'out_receipt':
            journal_type = ['sale']
        elif invoice_type == 'in_invoice' or invoice_type == 'in_refund' or invoice_type == 'in_receipt':
            journal_type = ['purchase']
        elif invoice_type == 'entry':
            journal_type = ['sale', 'purchase', 'cash', 'bank', 'general']


        if self.env.company.id == 4 and journal_type == 'sale':
            return [
                ('company_id', '=', self.env.company.id),
                ('branch_id', 'in', self.env.user.branch_ids.ids),
                ('type', 'in', journal_type)
            ]
        else:
            return [
                '&',
                ('company_id', '=', self.env.company.id),
                ('type','in', journal_type)
            ]

    branch_id = fields.Many2one('res.branch', string="Branch", domain=_allowed_branches)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 default=_get_default_journal,
                                 domain=_journal_branch_domain)

    @api.onchange('branch_id', 'user_id')
    def _branch_id(self):
        for data in self:
            if data.branch_id and data.company_id.id == 4 and data.type in ['out_invoice', 'out_refund', 'out_receipt']:
                journal_domain = data._journal_branch_domain()
                journal_domain += [('branch_id', '=', data.branch_id.id)]
                data.journal_id = False

                return {'domain': {'journal_id': journal_domain}}




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMoveLine, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')


        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({'branch_id' : branch_id})
        return res

    branch_id = fields.Many2one('res.branch', string="Branch")

AccountMove()