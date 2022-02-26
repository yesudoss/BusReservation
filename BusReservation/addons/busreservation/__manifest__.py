{
    'name': 'Bus Reservation',
    'version': '1.0',
    'category': 'Books',
    'sequence': 5,
    'summary': 'To maintain Reservation Details',
    'description': "",
    'website': '',
    'depends': [

    ],
    'data': [

        'security/bus_security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/templates.xml',

        # 'views/bus_search_view.xml',
        'views/report/reservation_invoice.xml',
        'views/reservations_view.xml',
        'views/locations_view.xml',
        'views/location_points_view.xml',
        'views/buses_view.xml',
        'views/routes_view.xml',
        'views/payment_view.xml',
        'views/member_view.xml',
        'views/res_users_view.xml',
        'views/client_actions_view.xml',
        'wizard/route_wizard_view.xml',
        'wizard/bus_wizard_view.xml',
        # 'wizard/pay_wizard_view.xml',
        'wizard/field_report_wizard_view.xml',
        'views/menu.xml',

    ],
    'demo': [
    ],
    'qweb': [
        "static/src/xml/*.xml"
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
