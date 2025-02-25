# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'FRESCOS Contacts',
    'category': '',
    'sequence': 150,
    'author': "soycalidad",
    'summary': 'Centralize your address book',
    'description': """
This module gives you a quick view of your contacts directory, accessible from your home page.
You can track your vendors, customers and other contacts.
""",
    'depends': ['base', 'mail'],
    'data': [
        'views/frescos_contact_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
