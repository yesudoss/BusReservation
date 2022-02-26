from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Buses(models.Model):
    _name = "buses.details"
    _description = "This is the table for Bus Details"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    number = fields.Char(string="Number", required=True)
    seats = fields.Integer(string="No of Seats", required=True)
    description = fields.Html(required=True)
