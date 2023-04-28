# -*- coding: utf-8 -*-
from odoo import fields,api,models

class EstafetaParcelCharge(models.Model):
    _name = 'estafeta.shipping.charge'
    _rec_name = 'estafeta_service_name'

    estafeta_service_name = fields.Char(string="Estafeta Service Name")
    estafeta_service_rate  = fields.Float(string="Estafeta Service Charge",help="Rate given by Easyparcel")
    sale_order_id = fields.Many2one("sale.order", string="Sales Order")

    def set_service(self):
        self.ensure_one()
        carrier = self.sale_order_id.carrier_id
        self.sale_order_id._remove_delivery_line()
        self.sale_order_id.estafeta_shipping_charge_id = self.id
        # self.sale_order_id.delivery_price = float(self.envia_total_price)
        self.sale_order_id.carrier_id = carrier.id
        self.sale_order_id.set_delivery_line(carrier, self.estafeta_service_rate)


