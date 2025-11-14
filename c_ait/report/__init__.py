from . import account_analytic_line_report
from . import working_hours_project_report
from . import project_task_report

from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    from datetime import date
    env = api.Environment(cr, SUPERUSER_ID, {})
    year = str(date.today().year)
    filter_rec = env.ref('your_module_name.filter_c_ait_analytic_line_report_this_year', raise_if_not_found=False)
    if filter_rec:
        filter_rec.domain = "[('date','>=','%s-01-01'),('date','<=','%s-12-31')]" % (year, year)
