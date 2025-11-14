from odoo import fields,models, api

class CAitPlanLine(models.Model):
    _name = 'c.ait.plan.line'

    plan_id = fields.Many2one(comodel_name='c.ait.plan', string='Plan')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    department_id = fields.Many2one(comodel_name='hr.department', string='Department')
    discipline_id = fields.Many2one(comodel_name='c.ait.discipline', string='Discipline')
    customer_partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    subcon_partner_id = fields.Many2one(comodel_name='res.partner', string='Subcontractor')
    plan_state = fields.Selection(related='plan_id.state', string='Plan State', store=True)
    plan_type = fields.Many2one(related='plan_id.type_id', store=True, string='Tip plana')
    date_from = fields.Date(related='plan_id.date_from', string='Od datuma', store=True)
    date_to = fields.Date(related='plan_id.date_to', string='Do datuma', store=True)
    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
    parent_task_id = fields.Many2one(comodel_name='project.task', string='Parent Task')
    milestone_id = fields.Many2one(comodel_name='project.milestone', string='Milestone')
    external_milestone_id = fields.Many2one(comodel_name='project.milestone', string='External Milestone')
    client_reference = fields.Char(string='Client Reference')
    number_hours = fields.Float(string='Hours')
    realized_hours = fields.Float(string='Realized Hours', compute='_compute_realized_hours', store=True)

    @api.depends()
    def _compute_realized_hours(self):
        for record in self:
            domain = [('date', '>=', record.date_from), ('date', '<=', record.date_to)]
            if record.employee_id:
                domain.append(('employee_id', '=', record.employee_id.id))
            if record.department_id:
                domain.append(('department_id', '=', record.department_id.id))
            if record.discipline_id:
                domain.append(('c_ait_discipline_id', '=', record.discipline_id.id))
            if record.subcon_partner_id:
                domain.append(('c_ait_subcon_id', '=', record.subcon_partner_id.id))
            if record.project_id:
                domain.append(('project_id', '=', record.project_id.id))
            if record.task_id:
                domain.append(('task_id', '=', record.task_id.id))
            if record.task_id and record.parent_task_id:
                domain.append(('task_id.parent_id', '=', record.parent_id.id))
            if record.task_id and record.milestone_id:
                domain.append(('task_id.milestone_id', '=', record.milestone_id.id))
            if record.task_id and record.external_milestone_id:
                domain.append(('task_id.c_ait_external_milestone_id', '=', record.external_milestone_id.id))
            if record.client_reference:
                domain.append(('task_id.c_ait_client_reference', '=', record.client_reference))

            analytic_lines = self.env['account.analytic.line'].search(domain=domain)
            record.realized_hours = sum(analytic_lines.mapped("unit_amount"))

