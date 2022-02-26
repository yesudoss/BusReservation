from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Routes(models.Model):
    _name = "routes.details"
    _description = "This is the table for Routes Details"
    # _rec_name = 'name'

    # name = fields.Char(string="Name")
    code = fields.Char(string="code")
    bus_id = fields.Many2one('buses.details', string="Bus", required=True)
    seats = fields.Integer(related="bus_id.seats", string="Total no of seats")
    count = fields.Char(string="Count / Booked Seats", compute="_compute_count")
    from_id = fields.Many2one('location.details', string="From")
    to_id = fields.Many2one('location.details', string="To")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    distance = fields.Char(string="Distance", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency Type")
    fare = fields.Monetary(string="Fare", required=True)
    description = fields.Html()

    # DEFAULT_GET ORM for Currency Symbol
    @api.model
    def default_get(self, fields):
        data = super(Routes, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data

    # NAME_GET ORM for Override rec_name
    def name_get(self):
        result = []
        for rec in self:
            if rec.from_id and rec.to_id and rec.fare:
                name = rec.from_id.name + ' - ' + rec.to_id.name + ' (₹ ' + str(rec.fare) + ')'
                result.append((rec.id, name))
        return result

    # Search Count ORM / COMPUTE COUNT ORM
    def _compute_count(self):
        # BROWSE ORM
        # unt = self.browse()
        # print(unt)
        self.count = self.env['reservations.details'].search_count([('route_id', '=', self.id)])


    # This is for Client Action II by Pradison
    @api.model
    def get_routes_info(self):
        # print(self)
        # print("Teacher Model")
        value = []
        data = self.env['routes.details'].search([])
        print(data)
        for rec in data:
            value.append({'from_id': rec.from_id.name, 'to_id': rec.to_id.name, 'bus_id': rec.bus_id.name, 'fare': rec.fare})
        print(value)
        return value