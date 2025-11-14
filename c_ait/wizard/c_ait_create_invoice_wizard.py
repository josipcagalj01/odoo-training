from odoo import fields, models, api
import datetime

class CAitCreateInvoiceWizard(models.TransientModel):
    _name = 'c.ait.create.invoice.wizard'

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    date_from = fields.Date(string='Od datuma', required=True)
    date_to = fields.Date(string='Do datuma', required=True)
    total_hours_worked = fields.Float(string='Total hours worked')
    total_hours_invoiced = fields.Float(string='Total hours invoiced')
    account_analytic_line_ids = fields.Many2many(comodel_name='account.analytic.line',string='Timesheets')
    partner_id = fields.Many2one(related='project_id.partner_id',string='Customer', store=True)
    invoice_date = fields.Datetime(string='Invoice Date')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal', domain=[('type', '=', 'sale')])
    created_invoice_account_move_id = fields.Many2one(comodel_name='account.move', string='Invoice')


    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id and 'project_id' in fields_list:
            res['project_id'] = active_id
        return res

    @api.onchange('date_to')
    def _onchange_date_to(self):
        for record in self:
            if record.date_to:
                if record.date_to.month == 12:
                    record.invoice_date = datetime.date(year=record.date_to.year+1, month=1,day=1) - datetime.timedelta(days=1)
                else:
                    record.invoice_date = datetime.date(year=record.date_to.year, month=record.date_to.month + 1, day=1) - datetime.timedelta(days=1)

    def action_fetch_timesheets(self):
        domain = [
            ('project_id', '=', self.project_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
        ]
        analytic_lines = self.env['account.analytic.line'].search(domain)

        self.total_hours_worked = sum(analytic_lines.mapped("unit_amount"))
        self.total_hours_invoiced = sum(analytic_lines.mapped("c_ait_billable_hours"))
        self.account_analytic_line_ids = analytic_lines.ids

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_create_invoice(self):
        invoice_lines = []

        unique_tariffs = []
        seen = []  # običan list

        for line in self.account_analytic_line_ids:
            tariff = line.c_ait_tariff_id
            if tariff and tariff.id not in seen:
                seen.append(tariff.id)
                unique_tariffs.append(tariff)

        for tariff in unique_tariffs:
            hours_to_invoice = sum(self.account_analytic_line_ids.filtered(lambda l: l.c_ait_tariff_id.id == tariff.id).mapped("c_ait_billable_hours"))
            invoice_lines.append((0,0,{
                'product_id': tariff.invoice_product_id.id,
                'name': f"{tariff.name} {tariff.invoice_product_id.name or 'Product 1'}",
                'quantity': hours_to_invoice,
                'price_unit': tariff.invoice_product_id.list_price,
                'account_id': tariff.invoice_product_id.property_account_income_id.id or
                              tariff.invoice_product_id.categ_id.property_account_income_categ_id.id,
                'tax_ids': [(6, 0, tariff.invoice_product_id.taxes_id.ids)],
            }))

        # Create invoice with two lines
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',  # Customer invoice
            'partner_id': self.partner_id.id,
            'invoice_date': self.invoice_date,
            'journal_id': self.journal_id.id,
            'invoice_date_due': self.invoice_date,
            'currency_id': self.env.company.currency_id.id,
            'invoice_line_ids': invoice_lines,
        })

        self.created_invoice_account_move_id = invoice

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

