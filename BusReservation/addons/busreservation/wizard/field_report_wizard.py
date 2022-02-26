from odoo import api, models, tools, fields, _


# This is main class
class FieldsWizard(models.TransientModel):
    _name = "field.wizard"
    _description = "This is the table for field wizard Details"
    # _rec_name = 'name'

    GENDER_LIST = [('male', 'Male'), ('female', 'Female'), ('others', 'Others')]

    route_id = fields.Many2one('routes.details', string="Route")
    gender = fields.Selection(GENDER_LIST, string="Gender", default='male')
    # train_id = fields.Many2one('train.details', string="Train Name")

    def field_wizard_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('acive_ids', [])
        data['active_model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['gender', 'route_id'])[0]
        return self.env.ref('busreservation.passengers_field_report').report_action(self, data=data)