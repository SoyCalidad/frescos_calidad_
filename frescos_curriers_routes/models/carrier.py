from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Carrier(models.Model):
    _name = 'custom.carrier'
    _description = 'Transportista'

    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    identification = fields.Char(string='Identificación', required=True)
    photo = fields.Image(max_width=128, max_height=128)
    vat = fields.Char(string='RFC', help="Registro Federal de Contribuyentes (RFC) Mexicano")
    position = fields.Char(string='Puesto', help='Puesto que ocupa el transportista')
    license = fields.Char(string='Licencia de Conducir', help="Número de licencia de conducir")
    active = fields.Boolean(string='Activo', default=True)
    
    @api.constrains('vat')
    def _check_vat(self):
        """
        Validación del RFC Mexicano.
        """
        for record in self:
            if record.vat and not self._validate_mexican_rfc(record.vat):
                raise ValidationError("El RFC ingresado no es válido: %s" % record.vat)

    @staticmethod
    def _validate_mexican_rfc(rfc):
        """
        Función para validar el formato del RFC mexicano.
        Formato: 3 o 4 letras + 6 dígitos (fecha YYMMDD) + 2 o 3 caracteres alfanuméricos.
        """
        import re
        pattern = r'^([A-ZÑ&]{3,4})\d{6}[A-Z0-9]{2,3}$'
        return bool(re.match(pattern, rfc))
    
    picking_ids = fields.One2many('stock.picking', 'carrier_id', string="Pickings Asignados") 
    picking_count = fields.Integer(string='Número de Pickings', compute='_get_picking_count', store=True)

    @api.depends('picking_ids')
    def _get_picking_count(self):
        for route in self:
            route.picking_count = len(route.picking_ids)

    def action_view_pickings(self):
        pickings = self.env['stock.picking'].search([('carrier_id', '=', self.id)])

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Stock Pickings Asignados',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('carrier_id', '=', self.id)],
            'context': {'create': False},
        }

        if not pickings:
            action['context'] = {'create': False, 'search_default_filter_empty': 1}
        return action
