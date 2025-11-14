from odoo import models
from collections import defaultdict
from datetime import datetime

class CAitProjectHoursReport(models.AbstractModel):
    _name = 'report.c_ait.report_project_hours_matrix'
    _description = 'Izvještaj radnih sati po projektu'

    def _get_report_values(self, docids, data=None):
        projects = self.env['project.project'].browse(docids)
        timesheets = self.env['account.analytic.line'].search([
            ('project_id', 'in', docids),
            ('employee_id', '!=', False),
        ])

        # Priprema matrice: {datum: {zaposlenik: sati}}
        matrix = defaultdict(lambda: defaultdict(float))
        employees = set()

        for line in timesheets:
            date = line.date
            employee = line.employee_id
            employees.add(employee)
            matrix[date][employee] += line.unit_amount

        sorted_dates = sorted(matrix.keys())
        sorted_employees = sorted(employees, key=lambda e: e.name)

        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'docs': projects,
            'matrix': matrix,
            'dates': sorted_dates,
            'employees': sorted_employees,
        }
