from odoo import fields, models, api
from datetime import datetime
from odoo .exceptions import UserError

class WizardReport(models.AbstractModel):
    _name = 'report.busreservation.passengers_field_template'
    # here 'report.passengers.field.report' is folder_name, addon_name and template_name

    def get_data(self, form_values):
        data = []
        # print(form_values['gender'])
        if form_values['gender']:
            recordsets = self.env['reservations.details'].search([('gender', '=', form_values['gender'])])

        if form_values['route_id']:
            tra_id = self.env['routes.details'].search([('id', '=', form_values['route_id'][0])])
            recordsets = self.env['reservations.details'].search([('route_id', '=', tra_id.id)])

        for recordsets in recordsets:
            data.append({
                'name': recordsets.name,
                'contact': recordsets.contact,
                'from_id': recordsets.from_id,
                'to_id': recordsets.to_id,
            })
        print(data)
        return data

    @api.model
    def _get_report_values(self, docsids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': docsids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'get_data': self.get_data(data['form']),
        }