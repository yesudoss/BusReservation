from odoo import models, fields, api, _

class BusUsers(models.Model):
    _inherit = "res.users"

    manager_id = fields.Many2one('member.details', string="Bus Reservations System Manager Name")
    # passenger_id = fields.Many2one('passenger.details', string="Passenger Name")