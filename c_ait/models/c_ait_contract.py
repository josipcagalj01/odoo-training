from odoo import models, fields

class CAitContract(models.Model):
    _name = 'c.ait.contract'
    _rec_name = 'number'

    number = fields.Char(string='Number')
    date = fields.Date(string='Date')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
