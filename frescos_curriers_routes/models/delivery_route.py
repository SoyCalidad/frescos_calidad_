from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeliveryRoute(models.Model):
    _name = 'delivery.route'
    _description = 'Delivery Routes'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    start_time = fields.Float(string='Hora Inicio', required=True, help="Hora en formato 24h (ejemplo: 13.5 para 1:30 PM)")
    end_time = fields.Float(string='Hora Fin', required=True, help="Hora en formato 24h (ejemplo: 18.0 para 6:00 PM)")
    
    active = fields.Boolean(string='Activo', default=True)
    truck_ids = fields.One2many('delivery.truck', 'route_id', string="Camiones Asignados")
    

    @api.constrains('start_time', 'end_time')
    def _check_schedule(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("La hora de inicio debe ser menor que la hora de fin.")
            
    picking_ids = fields.One2many('stock.picking', 'route_id', string="Pickings Asignados") 
    picking_count = fields.Integer(string='Número de Pickings', compute='_get_picking_count', store=True)

    @api.depends('picking_ids')
    def _get_picking_count(self):
        for route in self:
            route.picking_count = len(route.picking_ids)

    def action_view_pickings(self):
        pickings = self.env['stock.picking'].search([('route_id', '=', self.id)])

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Stock Pickings Asignados',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('route_id', '=', self.id)],
            'context': {'create': False},
        }

        if not pickings:
            action['context'] = {'create': False, 'search_default_filter_empty': 1}
        return action

    truck_count = fields.Integer(string='Número de Camiones', compute='_compute_truck_count', store=True)

    @api.depends('truck_ids')
    def _compute_truck_count(self):
        for route in self:
            route.truck_count = len(route.truck_ids)

    def action_view_trucks(self):
        trucks = self.env['delivery.truck'].search([('route_id', '=', self.id)])

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Camiones Asignados',
            'res_model': 'delivery.truck',
            'view_mode': 'tree,form',
            'domain': [('route_id', '=', self.id)],
            'context': {'create': False},
        }

        if not trucks:
            action['context'] = {'create': False, 'search_default_filter_empty': 1}
        return action
    