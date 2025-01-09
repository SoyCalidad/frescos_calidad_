from odoo import models, fields

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    manager_id = fields.Many2one('res.users', string="Manager")
    delivered_to = fields.Text(string="Entregado a")
