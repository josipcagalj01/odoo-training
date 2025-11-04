from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'
    c_ait_discipline_ids = fields.Many2many(comodel_name="c.ait.discipline", string='Discipline')