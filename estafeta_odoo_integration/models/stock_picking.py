from odoo import models, fields, api


class CorreosTrackingNumber(models.Model):
    _inherit = 'stock.picking'

    estafeta_parcel_status = fields.Char(string="Estafeta Parcel Status", copy=False)
    estafeta_number_of_labels = fields.Integer(string='Number of labels to print', default=2)