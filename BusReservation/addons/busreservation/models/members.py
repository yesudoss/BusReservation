from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Member(models.Model):
    _name = "member.details"
    _description = "This is the table for Member Details"
    _rec_name = 'name'

    GENDER_LIST = [('male', 'Male'), ('female', 'Female'), ('others', 'Others')]
    ROLE_LIST = [('manager', 'Manager')]

    name = fields.Char(string="Name", required=True)
    contact = fields.Char(string="Contact", required=True)
    mail = fields.Char(string="Email", required=True)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection(GENDER_LIST, string="Gender", required=True)
    role = fields.Selection(ROLE_LIST, string="Role", required=True)

    # code = fields.Char(string="code")
    country_id = fields.Many2one('res.country', string="Country", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    door_no = fields.Char(string="Door No", required=True)
    street = fields.Char(string="Street", required=True)
    city = fields.Char(string="City", required=True)
    # pin_code = fields.Char(string="Pin Code", required=True)

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
        data = super(Member, self).default_get(fields)
        country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
                                                        limit=1)
        if state_id:
            data['state_id'] = state_id.id
        print(state_id)
        if country_id:
            data['country_id'] = country_id.id or []
        return data
