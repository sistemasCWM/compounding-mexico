# -*- coding: utf-8 -*-
{
    'name': "Product Custom Label",

    'summary': """
        Print Customised product label""",

    'description': """
       Product Custom Label will allow you to customise the product label before print. You can create different 
       templates and use those templates to dynamically create  product labels.
       Also print separate labels for different product LOTs.
    """,

    'author': "Webveer",
    'category': 'Product',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['product', 'sale', 'stock'],

    # always loaded
    'data': [
        'report/custom_label_report.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/custom_label_view.xml',
        'report/custom_label_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.jpg'],
    'price': 50,
    'currency': 'EUR',
}
