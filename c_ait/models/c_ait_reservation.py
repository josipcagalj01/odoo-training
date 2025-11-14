from odoo import models, fields

class CAitReservation(models.Model):
    _name = 'c.ait.reservation'
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account'
    )
    date = fields.Datetime(string='Date')
    description = fields.Char(string='Description')
    type = fields.Selection(
        selection = [
            ('income', 'Prihod'),
            ('expense', 'Trošak')
        ],
        string = 'Reservation type'
    )
    status = fields.Selection(
        selection=[
            ('draft', 'Nacrt'),
            ('confirmed', 'Potvrđena'),
            ('posted', 'Proknjižena'),
            ('completed', 'Relizirana')
        ],
        default='draft',
        string='Reservation Status'
    )
    amount = fields.Float(string='Amount')

    def confirm_reservation(self):
        self.ensure_one()
        self.status = 'confirmed'
