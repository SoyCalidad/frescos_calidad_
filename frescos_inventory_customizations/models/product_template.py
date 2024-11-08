from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(
        selection_add=[('perishable', 'Perishable')],
        ondelete={'perishable': 'set default'}
    )

    @api.onchange('detailed_type')
    def _onchange_detailed_type(self):
        if self.detailed_type == 'perishable':
            self.type = 'product'  
        else:
            self.type = 'consu' 