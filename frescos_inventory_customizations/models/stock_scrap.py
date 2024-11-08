from odoo import models, fields

class ShrinkageReason(models.Model):
    _name = 'shrinkage.reason'
    _description = 'Shrinkage Reason'

    name = fields.Char(string="Reason", required=True)
    
class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    shrinkage_reason_id = fields.Many2one('shrinkage.reason', string="Shrinkage Reason")
