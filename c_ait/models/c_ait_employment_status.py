from odoo import models, fields

class CAitEmploymentStatus(models.Model):
    _name = 'c.ait.employment.status'
    name = fields.Char(string='Name')