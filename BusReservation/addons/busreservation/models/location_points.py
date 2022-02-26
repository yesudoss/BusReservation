from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning

class Points(models.Model):
    _name = "points.details"
    _description = "This is the table for Location Points Details"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    locations_id = fields.Many2one('location.details', string="Location", required=True)

    # DEFAULT_GET ORM for COUNTRY and STATE
    # @api.model
    # def default_get(self, fields):
    #     data = super(Points, self).default_get(fields)
        # classing_id = self.env['classing.details'].search([('class_code', '=', '1A')])
        # if classing_id:
        #     data['classing_id'] = classing_id.id

        # name = self.env['points.details'].search([('code', '=', 'locations_id.id')], limit=1)
        # if name:
        #     data['points.details'] =

        # country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        # state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
        #                                                 limit=1)
        # if state_id:
        #     data['state_id'] = state_id.id
        # if country_id:
        #     data['country_id'] = country_id.id or []
        # return data