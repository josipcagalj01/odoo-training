from odoo import models, fields

class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
    c_ait_partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    c_ait_is_external = fields.Boolean(string='Is Milestone External')
