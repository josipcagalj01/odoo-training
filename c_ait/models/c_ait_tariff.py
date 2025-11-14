from odoo import fields, models

class CAitTariff(models.Model):
    _name = 'c.ait.tariff'

    name = fields.Char(string='Name')
    hourly_rate = fields.Float(string='Hourly Rate')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    invoice_product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)