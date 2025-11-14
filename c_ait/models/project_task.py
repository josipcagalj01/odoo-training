from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _rec_name = 'name'

    c_ait_external_milestone_id = fields.Many2one(comodel_name='project.milestone', string='External milestone')
    c_ait_client_reference = fields.Char(related="project_id.c_ait_client_reference", store=True)