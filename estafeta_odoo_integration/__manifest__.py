{
    'name': 'Estafeta Shipping Integration',
    'category': 'Website',
    'author': "Vraja Technologies",
    'version': '14.0.23.11.21',
    'summary': """""",
    'description': """Our Odoo Estafeta Shipping Integration will help you connect with Estafeta Shipping Carrier with Odoo. automatically submit order information from Odoo to Estafeta and get Shipping label, and Order Tracking number from Estafeta to Odoo.we also providing gls,nacex,mrw,dhl spain shipping connector.""",
    'depends': ['delivery'],
    'live_test_url': 'https://www.vrajatechnologies.com/contactus',
    'data': ['views/res_company.xml',
             'security/ir.model.access.csv',
             'views/delivery_carrier.xml',
             #'views/sale_view.xml',
             'views/stock_picking.xml',

             ],
    'images': ['static/description/cover.png'],
    'maintainer': 'Vraja Technologies',
    'website': 'https://www.vrajatechnologies.com',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '321',
    'currency': 'EUR',
    'license': 'OPL-1',
}
# version changelog
# 14.0.01.09.2021 add office number field in company
# 14.0.23.11.21 change version log for manage erp
