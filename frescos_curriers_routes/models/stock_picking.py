from odoo import models, fields, api

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    
    partner_street = fields.Char(related='partner_id.street', string='Street', readonly=True)
    partner_street2 = fields.Char(related='partner_id.street2', string='Street 2', readonly=True)
    partner_city = fields.Char(related='partner_id.city', string='City', readonly=True)
    partner_state_id = fields.Many2one(related='partner_id.state_id', string='State', readonly=True)
    partner_zip = fields.Char(related='partner_id.zip', string='ZIP', readonly=True)
    partner_country_id = fields.Many2one(related='partner_id.country_id', string='Country', readonly=True)
    
    carrier_id = fields.Many2one(
        'custom.carrier', 
        string='Transportista', 
        domain=[('active', '=', True)],
        help="Selecciona el transportista para esta entrega."
    )
    
    truck_id = fields.Many2one(
        'delivery.truck', 
        string='Camión', 
        domain=[('active', '=', True)], 
        help="Selecciona el camión para esta entrega."
    )

    route_id = fields.Many2one(
        'delivery.route', 
        string='Ruta', 
        domain=[('active', '=', True)],
        help="Selecciona la ruta para esta entrega."
    )

    @api.onchange('route_id')
    def _onchange_route_id(self):
        if self.route_id:
            return {'domain': {'truck_id': [('route_id', '=', self.route_id.id), ('active', '=', True)]}}
        else:
            return {'domain': {'truck_id': [('active', '=', True)]}}
