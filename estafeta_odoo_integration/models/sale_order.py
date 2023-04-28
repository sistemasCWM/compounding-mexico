from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    estafeta_shipping_charge_ids = fields.One2many("estafeta.shipping.charge", "sale_order_id",
                                                   string="Estafeta Rate Matrix")
    estafeta_shipping_charge_id = fields.Many2one("estafeta.shipping.charge", string="Estafeta Service",
                                                  help="This Method Is Use Full For Generating The Label", copy=False)


    # def set_delivery_line(self):
    #     # Remove delivery products from the sales order
    #     self._remove_delivery_line()
    #     for order in self:
    #         if order.state not in ('draft', 'sent'):
    #             raise UserError(_('You can add delivery price only on unconfirmed quotations.'))
    #         elif not order.carrier_id:
    #             raise UserError(_('No carrier set for this order.'))
    #         elif not order.delivery_rating_success:
    #             raise UserError(_('Please use "Check price" in order to compute a shipping price for this quotation.'))
    #         else:
    #             price_unit = order.delivery_price
    #             # TODO check whether it is safe to use delivery_price here
    #             order._create_delivery_line(order.carrier_id, price_unit)
    #     return True
