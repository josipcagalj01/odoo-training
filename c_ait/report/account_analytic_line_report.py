from odoo import fields, models, tools

class AccountAnalyticLineReport(models.Model):
    _name = 'c.ait.analytic.line.report'
    _description = 'Account Analytic Report'
    _auto = False

    date = fields.Date(string='Date')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    amount = fields.Float(string='Amount')
    c_ait_billable_hours = fields.Float(string='Billable hours')
    unit_amount = fields.Float(string='Time spent')

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW c_ait_analytic_line_report AS (
                SELECT
                    aal.id AS id,
                    aal.date AS date,
                    aal.project_id AS project_id,
                    aal.task_id AS task_id,
                    aal.account_id AS account_id,
                    aal.amount AS amount,
                    aal.unit_amount AS unit_amount,
                    aal.c_ait_billable_hours AS c_ait_billable_hours
                FROM
                    account_analytic_line aal
                WHERE
                    aal.project_id IS NOT NULL
            )
        """)
