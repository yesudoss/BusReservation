from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Locations(models.Model):
    _name = "location.details"
    _description = "This is the table for Location Details"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="code", required=True)
    country_id = fields.Many2one('res.country', string="Country", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    # pin_code = fields.Char(string="Pin Code", required=True)

    # DEFAULT_GET ORM for COUNTRY and STATE
    @api.model
    def default_get(self, fields):
        data = super(Locations, self).default_get(fields)
        # classing_id = self.env['classing.details'].search([('class_code', '=', '1A')])
        # if classing_id:
        #     data['classing_id'] = classing_id.id

        country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
                                                        limit=1)
        if state_id:
            data['state_id'] = state_id.id
        if country_id:
            data['country_id'] = country_id.id or []
        return data