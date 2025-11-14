from odoo import models, fields

class CAitProjectEmployeeTariff(models.Model):
    _name = 'c.ait.project.employee.tariff'

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    tariff_id = fields.Many2one(comodel_name='c.ait.tariff', string='Tariff')