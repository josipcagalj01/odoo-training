from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    c_ait_discipline_id = fields.Many2one(comodel_name="c.ait.discipline", string='Discipline')
    c_ait_employment_status_id = fields.Many2many(comodel_name="c.ait.employment.status", string='Employment Status')

    # ova se metoda pokreće kad se na UI otvori novi element, npr account.analytic.line
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # na razini ORM-a je definirana bazna metoda default_get koja dohvaća neke osnovne vrijednosti i stavlja ih u dictionary. Mi tu metodu overrideamo i dodajemo neke svoje defualtne vrijednosti, i na kraju vraćamo res
        if "task_id" in res:

            task = self.env['project.task'].browse(res['task_id'])
            if task:
                project = task.project_id
                if project:
                    discipline = project.c_ait_discipline_id
                    if discipline:
                        res['c_ait_discipline_id'] = discipline.id
        return res