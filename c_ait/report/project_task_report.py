from odoo import models, fields, tools

class ProjectTaskReport(models.Model):
    _name = 'c.ait.project.task.report'
    _auto = False

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    milestone_id = fields.Many2one(comodel_name='project.milestone', string='Milestone')
    #description = fields.Char(string='Description')
    parent_id = fields.Many2one(comodel_name='project.task', string='Parent Task')
    allocated_hours = fields.Float(string='Allocated Hours')
    remaining_hours = fields.Float(string='Remaining Hours')
    name = fields.Char(string='Name')

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW c_ait_project_task_report AS (
                SELECT
                    pt.id AS id,
                    pt.project_id AS project_id,
                    pt.milestone_id AS milestone_id,
                    pt.name AS name,
                    pt.parent_id AS parent_id,
                    pt.allocated_hours AS allocated_hours,
                    pt.allocated_hours - (select sum(aal.amount) from account_analytic_line aal where task_id = pt.id) as remaining_hours
                FROM
                    project_task pt
                WHERE
                    pt.project_id IS NOT NULL
            )
        """)