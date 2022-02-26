from odoo import http, _
from odoo.http import request
# from odoo.addons.portal.controllers.portal import CustomerPortal
# from odoo.addons.website.controllers.main import Website
# from odoo import http
# from odoo.http import request
# from datetime import datetime, date
# from odoo.http import request
# import json


class ControllerClass(http.Controller):
    @http.route('/reservation', auth='public', type='http', website=True)
    def reserve_method(self, **kw):
        print("Controllers")
        sortby = None
        passenger_data = []
        # searchbar_sortings = {
        #     'data': {'label': _('Order Date'), 'order': 'data_order desc'},
        #     'name': {'label': _('Reference'), 'order': 'name'},
        #     'stage': {'label': _('Stage'), 'order': 'stage'}
        # }
        # if not sortby:
        #     sort_order = searchbar_sortings[sortby]['order']

        data = request.env['reservations.details'].search([])
        print(data)
        for rec in data:
            passenger_data.append({
                'name': rec.name,
                'contact': rec.contact,
                'from': rec.from_id.name,
                'to': rec.to_id.name,
                'tickets_no': rec.tickets_no,
                'total': rec.total,

            })
        print(passenger_data)
        return request.render("busreservation.template_buses", {'passenger_data': passenger_data})

    @http.route('/routes', auth='public', type='http', website=True)
    def rout_method(self, **kw):
        print("Controllers")
        sortby = None
        rout_data = []
        # searchbar_sortings = {
        #     'data': {'label': _('Order Date'), 'order': 'data_order desc'},
        #     'name': {'label': _('Reference'), 'order': 'name'},
        #     'stage': {'label': _('Stage'), 'order': 'stage'}
        # }
        # if not sortby:
        #     sort_order = searchbar_sortings[sortby]['order']

        data = request.env['routes.details'].search([])
        print(data)
        for rec in data:
            rout_data.append({
                'code': rec.code,
                'name': rec.bus_id.name,
                # 'seats': rec.bus_id.seats,
                # 'count': rec.count,
                'from': rec.from_id.name,
                'to': rec.to_id.name,
                'dep': rec.departure_time,
                'arr': rec.arrival_time,
                'distance': rec.distance,
                'fare': rec.fare,

            })
        print(rout_data)
        return request.render("busreservation.template_bus", {'rout_data': rout_data})

    @http.route('/reservation/create', auth='public', type='http', website=True)
    def create_passenger(self):
        reserve = request.env['reservations.details'].search([])
        location = request.env['location.details'].search([])
        points = request.env['points.details'].search([])
        pay = request.env['pay.details'].search([])
        currency = request.env['res.currency'].search([])
        state = request.env['res.country.state'].search([])
        country = request.env['res.country'].search([])
        routes = request.env['routes.details'].search([])
        data = [reserve, location, points, pay, currency, state, country, routes]
        return http.request.render('busreservation.create_new_reservation', {'data': data})

    @http.route('/reservation/save', auth='public', type='http', website=True)
    def save_new_passenger(self, **post):
        print(post)
        name = post['name']
        contact = post['contact']
        mail = post['mail']
        country = post['country_id']
        state = post['state_id']
        door_no = post['door_no']
        street = post['street']
        city = post['city']

        froms = post['from_id']
        to = post['to_id']
        route = post['route_id']
        board = post['board_id']
        drop = post['drop_id']
        dot = post['dot']
        tickets_no = post['tickets_no']

        country_id = request.env['res.country'].search([('name', '=', country)], limit=1)
        state_id = request.env['res.country.state'].search([('name', '=', state)], limit=1)
        from_id = request.env['location.details'].search([('name', '=', froms)], limit=1)
        to_id = request.env['location.details'].search([('name', '=', to)], limit=1)
        route_id = request.env['routes.details'].search([('code', '=', route)], limit=1)
        board_id = request.env['points.details'].search([('name', '=', board)], limit=1)
        drop_id = request.env['points.details'].search([('name', '=', drop)], limit=1)
        values = {
            'name': name,
            'contact': contact,
            'mail': mail,
            'country_id': country_id,
            'state_id': state_id,
            'door_no': door_no,
            'street': street,
            'city': city,
            'from_id': from_id,
            'to_id': to_id,
            'route_id': route_id,
            'board_id': board_id,
            'drop_id': drop_id,
        }
        request.env['reservations.details'].sudo().create(values)
        return http.request.render('busreservation.template_buses', {})