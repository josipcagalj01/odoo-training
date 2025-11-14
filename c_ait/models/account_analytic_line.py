from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    c_ait_discipline_id = fields.Many2one(comodel_name="c.ait.discipline", string='Discipline')
    c_ait_employment_status_id = fields.Many2one(comodel_name="c.ait.employment.status", string='Employment Status')
    c_ait_work_perspective_id = fields.Many2one(comodel_name='c.ait.work.perspective', string='Work Perspective')
    c_ait_invoice_status = fields.Selection(
        selection=[
            ('n_a', 'N/A'),
            ('not_invoiceable', 'Not invoiceable'),
            ('to_be_invoiced', 'To be invoiced'),
            ('invoice_draft', 'On a draft invoice'),
            ('invoice_posted', 'On a posted invoice'),
            ('invoice_paid', 'On a paid invoice')
        ],
        default='not_invoiceable',
        string='Invoice Status'
    )
    c_ait_billable_hours = fields.Float(string='Billable hours')
    c_ait_client_reference = fields.Char(string='Client Reference')
    c_ait_contract_id = fields.Many2one(comodel_name='c.ait.contract', string='Contract')
    c_ait_subcon_state = fields.Selection(
        selection=[
            ('draft', 'Nacrt'),
            ('confirmed', 'Potvrđen'),
            ('rejected', 'Odbijen'),
            ('invoiced', 'Fakturiran'),
        ],
        string='Subcontractor State'
    )
    c_ait_subcon_id = fields.Many2one(comodel_name='res.partner', string='Subcontractor')
    c_ait_project_partner_id = fields.Many2one(comodel_name='res.partner', related='project_id.partner_id', store=True, readonly=True)
    c_ait_project_allowed_tariff_ids = fields.Many2many(comodel_name='c.ait.tariff', string='Project Tariffs', related='project_id.c_ait_allowed_tariff_ids', readonly=True)
    c_ait_tariff_id = fields.Many2one(comodel_name='c.ait.tariff', string='Tariff')


    # ova se metoda pokreće kad se na UI otvori novi element, npr account.analytic.line
    @api.model
    def default_get(self, fields_list):
        _logger.info('default get')
        res = super().default_get(fields_list)
        # na razini ORM-a je definirana bazna metoda default_get koja dohvaća neke osnovne vrijednosti i stavlja ih u dictionary. Mi tu metodu overrideamo i dodajemo neke svoje defualtne vrijednosti, i na kraju vraćamo res
        _logger.info(res)
        _logger.info(self.env.context)
        context = self.env.context
        #  {'lang': 'en_US', 'tz': 'Europe/Zagreb', 'uid': 2, 'allowed_company_ids': [1], 'params': {'debug': 1, 'resId': 58, 'action': 'my-tasks', 'actionStack': [{'action': 'my-tasks'}, {'resId': 58, 'action': 'my-tasks'}]}, 'all_task': 0, 'default_user_ids': [[4, 2]]}
        # context.get('params', {}).get('resId') and context.get('params', {}).get('action') == "my-tasks"
        if 'task_id' in res:
            #task_id = context['params']['resId']


            task = self.env['project.task'].browse(res["task_id"])
            if task:
                project = task.project_id
                if project:
                    disciplines = project.c_ait_discipline_ids
                    _logger.info(disciplines)
                    if disciplines:
                        res['c_ait_discipline_id'] = disciplines.ids[0]
                    perspective = project.c_ait_work_perspective_id
                    if perspective:
                        res['c_ait_work_perspective_id'] = perspective.id
                    contract = project.c_ait_contract_id
                    if contract:
                        res['c_ait_contract_id'] = project.c_ait_contract_id
                    client_refrerence = project.c_ait_client_reference
                    if client_refrerence:
                        res['c_ait_client_reference'] = project.c_ait_client_reference
                    #tariff = project.c_ait_tariff_id
                    #if tariff:
                    #    res['c_ait_tariff_id'] = project.c_ait_tariff_id

        _logger.info("JOSIPJOSIP")
        _logger.info(res)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('project_id'):
                project = self.env['project.project'].browse(vals['project_id'])
                if project.c_ait_contract_id:
                    vals['c_ait_contract_id'] = project.c_ait_contract_id.id
                if project.c_ait_client_reference:
                    vals['c_ait_client_reference'] = project.c_ait_client_reference
            if vals.get('c_ait_subcon_id') and not vals.get('c_ait_subcon_state'):
                vals['c_ait_subcon_state'] = 'draft'
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if 'project_id' in vals:
                record.c_ait_contract_id = record.project_id.c_ait_contract_id
                record.c_ait_client_reference = record.project_id.c_ait_client_reference
            if 'c_ait_subcon_id' in vals and not record.c_ait_subcon_state:
                record.c_ait_subcon_state = 'draft'
        return res

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for record in self:
            if record.employee_id:
                record.c_ait_employment_status_id = record.employee_id.c_ait_employment_status_id
                tariff_line = record.project_id.c_ait_project_employee_tariff.filtered(
                    lambda l: l.tariff_id.id in record.c_ait_project_allowed_tariff_ids.ids and l.employee_id==record.employee_id
                )[:1]
                record.c_ait_tariff_id = tariff_line.tariff_id.id if tariff_line else False

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for record in self:
            if record.project_id:
                record.c_ait_discipline_id = record.project_id.c_ait_discipline_ids.ids[0]
                record.c_ait_work_perspective_id = record.project_id.c_ait_work_perspective_id
                record.c_ait_client_reference = record.project_id.c_ait_client_reference
                record.c_ait_contract_id = record.project_id.c_ait_contract_id

    @api.onchange('c_ait_subcon_id')
    def _onchange_subcon_id(self):
        _logger.info('Subcontractor State')
        for record in self:
            _logger.info(record.c_ait_subcon_state)
            if record.c_ait_subcon_id and (not record.c_ait_subcon_state):
                record.c_ait_subcon_state = 'draft'
