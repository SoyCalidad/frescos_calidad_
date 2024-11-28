# -*- coding: utf-8 -*-
{
    'name': "Personalizar Rutas",

    'summary': """
        Personaliza rutas, transportistas, camiones""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',
                'stock',
                'sign',],

    'data': [
        'security/ir.model.access.csv',
        'views/carrier_views.xml',
        'views/stock_picking_views.xml',
        'views/delivery_route_views.xml',
        'views/delivery_truck_views.xml',
    ],
}