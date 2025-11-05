from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'
    c_ait_external_milestone_id = fields.Many2one(comodel_name='project.milestone', string='External milestone')