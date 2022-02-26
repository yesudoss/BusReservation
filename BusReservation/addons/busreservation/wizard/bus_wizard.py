from odoo import models, fields

class BusWizard(models.TransientModel):
    _name = 'buses.wizard'
    _description = "This is the table for Route wizard"
    _rec_name = 'name_id'

    name_id = fields.Many2one('buses.details', string="Name", required=True)
    number = fields.Char(string="Number", required=True)
    seats = fields.Integer(string="No of Seats", required=True)
    description = fields.Html(string="Description", required=True)

    def update_bus(self):
        print("Updated")
        return self.name_id.write({'number': self.number, 'seats': self.seats, 'description':self.description})