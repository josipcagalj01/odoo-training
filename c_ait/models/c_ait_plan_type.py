from odoo import fields, models

class CAitPlanType(models.Model):
    _name = 'c.ait.plan.type'

    name = fields.Char(required=True)
