from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning
from odoo.osv import expression
from lxml import etree
import json
class Reservations(models.Model):
    _name = "reservations.details"
    _description = "This is the table for Reservation Details"
    _rec_name = 'name'

    GENDER_LIST = [('male', 'Male'), ('female', 'Female'), ('others', 'Others')]

    STATUS_LIST = [('draft', 'Draft'), ('confirm', 'Confirmed'), ('cancel', 'Cancelled'), ('done', 'Done')]

    BLOOD_LIST = [('a-', 'A-'), ('a+', 'A+'), ('b-', 'B-'), ('b+', 'B+'), ('o-', 'O-'), ('o+', 'O+'), ('ab-', 'AB-'),
                  ('ab+', 'AB+')]

    name_seq = fields.Char(string="Reservation Reference", required=True, readonly=True, copy=False,
                           index=True, default=lambda self: _('New'))
    name = fields.Char(string="Name", required=True)
    # profile = fields.Binary()
    # aadhar = fields.Char(string="Aadhar Number", required=True)
    contact = fields.Char(string="Contact", required=True)
    mail = fields.Char(string="Email", required=True)
    gender = fields.Selection(GENDER_LIST, string="Gender")
    dob = fields.Date(string="Date of Birth")
    blood_group = fields.Selection(BLOOD_LIST, string="Blood Group")
    country_id = fields.Many2one('res.country', string="Country", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    door_no = fields.Char(string="Door No", required=True)
    street = fields.Char(string="Street", required=True)
    city = fields.Char(string="City", required=True)

    from_id = fields.Many2one('location.details', required=True)
    board_id = fields.Many2one('points.details', required=True, string="Boarding Point")
    to_id = fields.Many2one('location.details', required=True)
    drop_id = fields.Many2one('points.details', required=True, string="Drop Point")
    tickets_no = fields.Integer(string="No of Tickets", required=True)
    currency_id = fields.Many2one('res.currency')
    total = fields.Monetary(string="Total", compute="_calculate_total", store=True)
    dot = fields.Date(required=True)
    payment_id = fields.Many2one('pay.details')
    route_id = fields.Many2one('routes.details', string="Available Buses", required=True)
    status = fields.Selection(STATUS_LIST, string="Status", default='draft')
    # payment_id = fields.Many2one('pay.details')
    # status_id = fields.Selection(related="payment_id.status", string="Payment Status")

    # CONSTRAINS DEOCRATOR for EMAIL Validation
    @api.constrains('mail')
    def validate_mail(self):
        if self.mail and not tools.single_email_re.match(self.mail):
            raise ValidationError("Email is not valid")


    @api.constrains('contact')
    def _check_phone_number(self):
        for rec in self:
            if rec.contact and len(rec.contact) != 10 and not str(rec.contact).isdigit():
                raise ValidationError(_("Enter Valid Mobile Number..."))
        return True

    # DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(Reservations, self).default_get(fields)
        # classing_id = self.env['classing.details'].search([('class_code', '=', '1A')])
        # if classing_id:
        #     data['classing_id'] = classing_id.id

        # status_id = self.env['pay.details'].search([('status', '=', 'paid')])

        country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
                                                        limit=1)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id

        if state_id:
            data['state_id'] = state_id.id
        print(state_id)
        if country_id:
            data['country_id'] = country_id.id or []
        return data


    # THIS IS for STATUS BAR
    def action_draft(self):
        if self.status:
            print(self.status)
            self.status = "draft"
    # def action_confirm(self):
    #     if self.status:
    #         print(self.status)
    #         self.status = "confirm"
    def action_cancel(self):
        if self.status:
            print(self.status)
            self.status = "cancel"
    def action_done(self):
        if self.status:
            print(self.status)
            self.status = "done"
        # ONCHANGE DECORATOR

    # @api.onchange('payment_id')
    # def _onchange_is_dob(self):
    #     if self.status_id == 'paid':
    #         self.status = 'confirm'
        # else:
        #     self.dob = ''
        #     self.age1 = ''

    # DEPENDS Decorator to calculate Total amount
    @api.depends('tickets_no')
    def _calculate_total(self):
        for rec in self:
            if rec.tickets_no:
                rec.total = rec.route_id.fare * rec.tickets_no
            # self.age1 = datetime.now().year - self.dob.year()

    # CREATE ORM FOR SEQUENCE
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('reservations.sequence') or _('New')
        result = super(Reservations, self).create(vals)
        return result


        # This is for Client Action II by Pradison
    @api.model
    def get_reservation_info(self):
        # print(self)
        # print("Teacher Model")
        value = []
        data = self.env['reservations.details'].search([])
        print(data)
        for rec in data:
            value.append({'name': rec.name, 'contact': rec.contact})
        print(value)
        return value


        #     UNLINK ORM
    def unlink(self):
        for rec in self:
            if rec.status in ['confirm', 'done']:
                raise ValidationError(_("You cannot delete these confirmed / Completed records"))
            return super(Reservations, self).unlink()

    # # FIELDS_VIEW_GET ORM
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(Reservations, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #
    #     if self.user_has_groups("busreservation.passengers_passenger_role"):
    #         if view_type == 'form':
    #             # Remove the if statement if you want to make changes in every view
    #             for node in doc.xpath("//field[@name='train_code']"):
    #                 modifiers = json.loads(node.get('modifiers'))
    #                 modifiers['readonly'] = True
    #                 node.set("modifiers", json.dumps(modifiers))
    #     if self.user_has_groups("passengers.passengers_passenger_role"):
    #         for view in doc.xpath("//"+view_type):
    #             # view.attrib['create'] = 'false'
    #             # view.attrib['delete'] = 'false'
    #             view.attrib['edit'] = 'false'
    #
    #     res['arch'] = etree.tostring(doc, encoding='unicode')
    #     return res