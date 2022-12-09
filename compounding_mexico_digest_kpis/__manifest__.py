# -*- coding: utf-8 -*-

{
    'name': 'Mexico Compounding : NEW KPIS for Odoo Digest Email',
    'summary': 'Adds new KPIs to the digest emails.',
    'license': 'OPL-1',
    'website': 'https://www.odoo.com',
    'version': '1.0',
    'author': 'Odoo Inc',
    'description': """
        Mexico Compounding : NEW KPIS for Odoo Digest Email
        Task ID: 2937374
        Addition of three KPIs to Odoo Digest Email:
        - Confirmed Sales by Salesperson.
        - Confirmed sales of new clients.
        - Bank account balance in General Ledger.
    """,
    'category': 'Custom Development',
    'depends': [
        'digest',
        'sale_management',
        'account',
        'account_accountant'
    ],
    'data': [
        'data/digest_data.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}