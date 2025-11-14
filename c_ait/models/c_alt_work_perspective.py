from odoo import fields, models

class CAitWorkPerspective(models.Model):
    _name = 'c.ait.work.perspective'
    name = fields.Char(string='Name')