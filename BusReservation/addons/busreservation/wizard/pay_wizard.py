from odoo import models, fields, api, _

class PayWizard(models.TransientModel):
    _name = 'pays.wizard'
    _description = "This is the table for Payment wizard"
    _rec_name = 'name_id'

    # name_id = fields.Many2one('buses.details', string="Name", required=True)
    # number = fields.Char(string="Number", required=True)
    # seats = fields.Integer(string="No of Seats", required=True)
    # description = fields.Html(string="Description", required=True)

    name_id = fields.Many2one('pay.details')

    currency_id = fields.Many2one('res.currency')
    # name_seq_id = fields.Char(related="name_id.name_seq", readonly="True", string="Reference ID")
    tickets_no = fields.Integer(string="No of Tickets", related="name_id.tickets_no", store=True)
    total = fields.Monetary(string="Total Amount", related="name_id.total", store=True)


    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(PayWizard, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
            return data

    def create_payment(self):
        print("Created")
        return self.name_id.create({'name_id': self.name_id.name, 'tickets_no': self.tickets_no, 'total': self.total})