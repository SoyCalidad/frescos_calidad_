from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime

class DeliveryTruckExpense(models.Model):
    _name = 'delivery.truck.expense'
    _description = 'Delivery Truck Expense'

    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)
    truck_id = fields.Many2one('delivery.truck', string="Camión", required=True, ondelete="cascade")
    description = fields.Char(string="Descripción", required=True)
    date = fields.Date(string="Fecha", required=True, default=fields.Date.context_today)
    amount = fields.Float(string="Monto", required=True)


class DeliveryTruck(models.Model):
    _name = 'delivery.truck'
    _description = 'Delivery Trucks'

    name = fields.Char(string='Nombre', required=True)
    license_plate = fields.Char(string='Placa', required=True)
    security_number = fields.Char(string='Numero de Seguro', required=True)
    expiration_date = fields.Date(string='Fecha de Expiración del Seguro', required=True)
    brand_model = fields.Char(string='Marca y Modelo', required=True)
    capacity = fields.Float(string='Capacidad (Toneladas)', help='Capacidad máxima en toneladas')
    photo = fields.Image(max_width=128, max_height=128)
    active = fields.Boolean(string='Activo', default=True)
    expense_ids = fields.One2many('delivery.truck.expense', 'truck_id', string="Gastos Relacionados Reales")
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)
    route_id = fields.Many2one('delivery.route', string="Ruta Asignada", ondelete='restrict')
    
    total_expense = fields.Float(
        string="Gastos Totales", 
        compute="_compute_total_expense", 
        store=True
    )
    
    
    @api.depends('expense_ids')
    def _compute_total_expense(self):
        for truck in self:
            truck.total_expense = sum(expense.amount for expense in truck.expense_ids)
            
    
    picking_ids = fields.One2many('stock.picking', 'truck_id', string="Pickings Asignados") 
    picking_count = fields.Integer(string='Número de Pickings', compute='_get_picking_count', store=True)

    @api.depends('picking_ids')
    def _get_picking_count(self):
        for route in self:
            route.picking_count = len(route.picking_ids)

    def action_view_pickings(self):
        pickings = self.env['stock.picking'].search([('truck_id', '=', self.id)])

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Stock Pickings Asignados',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('truck_id', '=', self.id)],
            'context': {'create': False},
        }

        if not pickings:
            action['context'] = {'create': False, 'search_default_filter_empty': 1}
        return action
