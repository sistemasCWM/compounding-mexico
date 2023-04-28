from odoo import fields,api,models

class ResCompany(models.Model):
    _inherit = "res.company"

    estafeta_api_url = fields.Char(string="Estafeta API URL", help="Enter Estafeta API URL")
    estafeta_username = fields.Char(string="Estafeta Username",help="Enter Your Estafeta Account's Username")
    estafeta_password = fields.Char(string="Estafeta Password",help="Enter Your Estafeta Account's Password")
    estafeta_office_number = fields.Char(string='Estafeta Office Number', help='Enter Estafeta Office Number')
    estafeta_suscriberId = fields.Char(string="Estafeta Service Subscriber Identifier",help="Enter Your Estafeta Account's Service Subscriber Identifier")
    estafeta_customer_number = fields.Char(string="Estafeta Customer Number", help="Enter Your Estafeta Account's Customer Number")
    use_estafeta_shipping_provider = fields.Boolean(copy=False, string="Are You Using Estafeta?",
                                               help="If use Estafeta shipping Integration than value set TRUE.",
                                               default=False)
    estafeta_rate_api_username = fields.Char(string="Estafeta Rate API Username", help="Enter Your Estafeta Account's Username")
    estafeta_rate_api_password = fields.Char(string="Estafeta Rate API Password", help="Enter Your Estafeta Account's Password")

