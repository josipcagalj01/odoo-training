from odoo import models, fields

class CAitDiscipline(models.Model):
    _name = 'c.ait.discipline'
    name = fields.Char(string='Name')