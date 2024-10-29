# -*- coding: utf-8 -*-
{
    'name': "Personalizar Inventario",

    'summary': """
        Personaliza inventario Frescos""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',
                'stock',
                'hr',
                'purchase',
                'product',
                'report_xlsx',],

    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/stock_picking_templates.xml',
        'views/shrinkage_reason_views.xml',
        'views/stock_scrap_views.xml',
        'views/purchase_order_views.xml',
        
        'report/popularity_table_wizard_view.xml',
        'report/popularity_table_xlsx.xml',
        'report/menu.xml',
    ],
}