from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Payment(models.Model):
    _name = "pay.details"
    _description = "This is the table for Payment Details"
    _rec_name = 'name_id'

    STATUS_LIST = [('paid', 'Paid'), ('not_paid', 'Not Paid')]

    name_id = fields.Many2one('reservations.details')

    currency_id = fields.Many2one('res.currency')
    # name_seq_id = fields.Char(related="name_id.name_seq", readonly="True", string="Reference ID")
    tickets_no = fields.Integer(string="No of Tickets", related="name_id.tickets_no", store=True)
    total = fields.Monetary(string="Total Amount", related="name_id.total", store=True)
    # status = fields.Selection(STATUS_LIST, string="Status", default='not_paid')

    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(Payment, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
            return data

# THIS IS for STATUS BAR
#     def action_not_paid(self):
#         if self.status:
#             print(self.status)
#             self.status = "not_paid"
#     def action_paid(self):
#         if self.status:
#             print(self.status)
#             self.status = "paid"
