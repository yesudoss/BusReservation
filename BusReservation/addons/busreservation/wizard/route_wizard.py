from odoo import api, models, tools, fields, _

class RoutWizard(models.TransientModel):
    _name = 'rout.wizard'
    _description = "This is the table for Route wizard"
    # _rec_name = 'route_id'

    route_id = fields.Many2one('routes.details', string="Route")

    code = fields.Char(string="code")
    bus_id = fields.Many2one('buses.details', string="Bus", required=True)
    from_id = fields.Many2one('location.details', string="From")
    to_id = fields.Many2one('location.details', string="To")
    # departure_time = fields.Datetime()
    # arrival_time = fields.Datetime()
    distance = fields.Char(string="Distance", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency Type")
    fare = fields.Monetary(string="Fare", required=True)
    # description = fields.Html()
    # # reservation_fee = fields.Integer(string="Reservation Fee (GST)")

    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(RoutWizard, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
            return data

    def update_route(self):
        print("Updated")
        return self.route_id.write({'code': self.code, 'bus_id': self.bus_id, 'from_id': self.from_id, 'to_id': self.to_id, 'distance': self.distance, 'fare': self.fare})

