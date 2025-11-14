from odoo import models, fields

class CAitHrEmployee(models.Model):
    _inherit = 'hr.employee'
    c_ait_employment_status_id = fields.Many2one(comodel_name='c.ait.employment.status', string='Employment Status')