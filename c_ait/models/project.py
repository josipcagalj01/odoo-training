from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    c_ait_discipline_ids = fields.Many2many(comodel_name="c.ait.discipline", string='Discipline')
    c_ait_client_reference = fields.Char(string='Client reference')
    c_ait_work_perspective_id = fields.Many2one(comodel_name='c.ait.work.perspective', string='Work Perspective', help='Defines the methodology or strategic approach of the project')
    c_ait_contract_id = fields.Many2one(comodel_name='c.ait.contract', string='Contract')
    c_ait_tariff_id = fields.Many2one(comodel_name='c.ait.tariff', string='Tariff')
    c_ait_end_user_partner_id = fields.Many2one(comodel_name='res.partner', string='End User')
    c_ait_allowed_tariff_ids = fields.Many2many(comodel_name='c.ait.tariff', string='Allowed Tariffs')
    c_ait_employee_tariff_ids = fields.Many2one(comodel_name='c.ait.project.employee.tariff', string='Employee Tariffs')
    c_ait_project_employee_tariff = fields.One2many(comodel_name='c.ait.project.employee.tariff', string='Tariff', inverse_name='project_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('partner_id') and not vals.get('c_ait_end_user_partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                vals['c_ait_end_user_partner_id'] = partner.id
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if 'partner_id' in vals and not record.c_ait_end_user_partner_id:
                record.c_ait_end_user_partner_id = record.partner_id
        return res

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            if record.partner_id and not record.c_ait_end_user_partner_id:
                record.c_ait_end_user_partner_id = record.partner_id