from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    expiration_date = fields.Date(string="Expiration Date")
    perishable = fields.Boolean(string="Perishable", default=False)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self: 
            if line.product_id.detailed_type == 'perishable':
                line.perishable =  True
            else:
                line.perishable =  False