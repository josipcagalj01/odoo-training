from odoo import fields, models

class CAitPlan(models.Model):
    _name = 'c.ait.plan'

    name = fields.Char(string='Name')
    period_type = fields.Selection(
        selection = [
            ('day', 'Dnevni'),
            ('week', 'Tjedni'),
            ('month', 'Mjesečni'),
            ('quarter', 'Kvartalni'),
            ('year', 'Godišnji')
        ],
        string='Period'
    )
    date_from = fields.Date(string='Od datuma', required=True)
    date_to = fields.Date(string='Do datuma', required=True)
    planned_amount = fields.Float(string='Planned amount')
    state = fields.Selection(
        selection = [
            ('draft', 'Draft'),
            ('planned', 'Planned'),
            ('active', 'Active'),
            ('inactive', 'Inactive')
        ],
        default='draft',
        string='State'
    )
    type_id = fields.Many2one(comodel_name='c.ait.plan.type', string='Type')
    line_ids = fields.One2many(comodel_name='c.ait.plan.line', string='Lines', inverse_name='plan_id')

    def set_state_planned(self):
        self.ensure_one()
        self.state = 'planned'
