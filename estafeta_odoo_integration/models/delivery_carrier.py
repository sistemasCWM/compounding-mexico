# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
import logging
import requests
import binascii
import xml.etree.ElementTree as etree
from odoo.exceptions import ValidationError
from odoo.addons.estafeta_odoo_integration.models.estafeta_response import Response

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(selection_add=[("estafeta", "Estafeta")], ondelete={'estafeta': 'set default'})
    service_code = fields.Char(string="Service Code", help="see list of services with your sales consultant",
                               default="70")
    estafeta_packaging_id = fields.Many2one('product.packaging', string="Default Package Type")
    deliver_to_estafeta_office = fields.Boolean(string="Delivery To Estafeta Office",
                                                help="If deliveryToEstafetaOffice value is True, the shipment is  Occur delivery that means that the shipment will be delivered to an estafeta office")
    estafeat_parcel_type_id = fields.Selection([('1', 'Envelope'), ('4', 'Package')],
                                               string="Estafeta Parcel Type Id", help="Type of shipment")
    estafeat_return_documnet = fields.Boolean(string="Estafeta Return Document",
                                              help="Field that tells if the shipment requires an additional waybill  return document ")
    estafeta_paper_type = fields.Selection([('1', 'Letter size Bond paper'),
                                            ('2', '6 x 4 inches size Thermal label paper'),
                                            ('3', 'Legal size 4 labels template')],
                                           string='Label Type')

    # estafeta_number_of_labels = fields.Integer(string='Number of labels to print', default=1)

    def estafeta_rate_data(self, order=False):
        """This Method Return"""
        # origin_zipcode = order.warehouse_id and order.warehouse_id.partner_id.zip
        # destination_zipcode = order.partner_shipping_id.zip
        #
        # if not origin_zipcode:
        #     raise ValidationError("Please Define Origin Zip Code")
        #
        # if not destination_zipcode:
        #     raise ValidationError("Please Define Destination Zip Code")
        #
        # if self.estafeat_parcel_type_id == '1':
        #     espaquete = True
        # else:
        #     espaquete = False
        #
        # total_weight = sum([(line.product_id.weight * line.product_uom_qty) for line in order.order_line]) or 0.0
        #
        # master_node = etree.Element('soap:Envelope')
        # master_node.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        # master_node.attrib['xmlns:xsd'] = 'http://www.w3.org/2001/XMLSchema'
        # master_node.attrib['xmlns:soap'] = 'http://schemas.xmlsoap.org/soap/envelope/'
        # master_node_body = etree.SubElement(master_node, 'soap:Body')
        # sub_master_node_FrecuenciaCotizador = etree.SubElement(master_node_body, 'FrecuenciaCotizador')
        # sub_master_node_FrecuenciaCotizador.attrib['xmlns'] = 'http://www.estafeta.com/'
        # etree.SubElement(sub_master_node_FrecuenciaCotizador, 'idusuario').text = '{}'.format(
        #     self.company_id and self.company_id.estafeta_customer_number)
        # etree.SubElement(sub_master_node_FrecuenciaCotizador, 'usuario').text = '{}'.format(
        #     self.company_id and self.company_id.estafeta_rate_api_username)
        # etree.SubElement(sub_master_node_FrecuenciaCotizador, 'contra').text = '{}'.format(
        #     self.company_id and self.company_id.estafeta_rate_api_password)
        # etree.SubElement(sub_master_node_FrecuenciaCotizador, 'esFrecuencia').text = 'true'
        # etree.SubElement(sub_master_node_FrecuenciaCotizador, 'esLista').text = 'true'
        # sub_master_node_tipoEnvio = etree.SubElement(sub_master_node_FrecuenciaCotizador, 'tipoEnvio')
        # etree.SubElement(sub_master_node_tipoEnvio, 'EsPaquete').text = '{}'.format(espaquete).lower()
        # if espaquete == True:
        #     etree.SubElement(sub_master_node_tipoEnvio, 'Largo').text = "{}".format(
        #         self.estafeta_packaging_id.packaging_length)  # Long
        #     etree.SubElement(sub_master_node_tipoEnvio, 'Peso').text = "{}".format(total_weight)  # Weight
        #     etree.SubElement(sub_master_node_tipoEnvio, 'Alto').text = "{}".format(
        #         self.estafeta_packaging_id.height)  # height
        #     etree.SubElement(sub_master_node_tipoEnvio, 'Ancho').text = "{}".format(
        #         self.estafeta_packaging_id.width)  # width
        # sub_master_node_dataorigen = etree.SubElement(sub_master_node_FrecuenciaCotizador, 'datosOrigen')
        # etree.SubElement(sub_master_node_dataorigen, 'string').text = '{}'.format(origin_zipcode)
        # sub_master_node_datosDestino = etree.SubElement(sub_master_node_FrecuenciaCotizador, 'datosDestino')
        # etree.SubElement(sub_master_node_datosDestino, 'string').text = '{}'.format(destination_zipcode)
        # return etree.tostring(master_node)

    def estafeta_rate_shipment(self, order):
        # estafeta_shippig_charg_obj = self.env['estafeta.shipping.charge']
        # data = self.estafeta_rate_data(order)
        # _logger.info(data)
        # api_url = 'http://frecuenciacotizador.estafeta.com/Service.asmx'
        # headers = {
        #     "Content-Type": "text/xml; charset=utf-8",
        #     "SOAPAction": "http://www.estafeta.com/FrecuenciaCotizador"
        # }
        # try:
        #     response_data = requests.post(url=api_url, data=data, headers=headers)
        #     if response_data.status_code in [200, 201]:
        #         _logger.info("Get Successfully 200 Response From {}".find(api_url))
        #
        #         existing_records = estafeta_shippig_charg_obj.sudo().search(
        #             [('sale_order_id', '=', order and order.id)])
        #         existing_records.sudo().unlink()
        #         response_data = Response(response_data)
        #         result = response_data.dict()
        #         _logger.info(result)
        #         rate_datas = result.get('Envelope').get('Body').get('FrecuenciaCotizadorResponse').get(
        #             'FrecuenciaCotizadorResult').get('Respuesta').get('TipoServicio')
        #         if not rate_datas:
        #             return {'success': False, 'price': 0.0, 'error_message': "Rate Not Found! %s" % (result),
        #                     'warning_message': False}
        #         if isinstance(rate_datas, dict):
        #             rate_datas = [rate_datas]
        #         for rate_data in rate_datas:
        #             _logger.info("In for Loop")
        #             for rate in rate_data.get('TipoServicio'):
        #                 estafeta_service_name = rate.get('DescripcionServicio')
        #                 estafeta_service_rate = rate.get('CostoTotal')
        #                 estafeta_shippig_charg_obj.sudo().create(
        #                     {'estafeta_service_name': estafeta_service_name,
        #                      'estafeta_service_rate': estafeta_service_rate,
        #                      'sale_order_id': order and order.id})
        #         estafeta_shipping_charge_id = estafeta_shippig_charg_obj.sudo().search(
        #             [('sale_order_id', '=', order and order.id)], order='estafeta_service_rate', limit=1)
        #         order.estafeta_shipping_charge_id = estafeta_shipping_charge_id and estafeta_shipping_charge_id.id
        #
        #         return {'success': True,
        #                 'price': estafeta_shipping_charge_id and estafeta_shipping_charge_id.estafeta_service_rate or 0.0,
        #                 'error_message': False, 'warning_message': False}
        #     else:
        #         return {'success': False, 'price': 0.0, 'error_message': "%s %s" % (response_data, response_data.text),
        #                 'warning_message': False}
        # except Exception as e:
        return {'success': True, 'price': 0.0, 'error_message': False, 'warning_message': False}

    def estafeta_label_request_data(self, picking=False):
        sender_id = self.company_id
        receiver_id = picking.partner_id
        sender_phone = sender_id and sender_id.phone
        receiver_phone = receiver_id and receiver_id.phone
        office_number = self.company_id and self.company_id.estafeta_office_number
        if not sender_phone:
            raise ValidationError("Please Define Sender Phone Number")
        else:
            if '+' in sender_id.phone:
                sender_phone = sender_id.phone.replace('+', '')
        if not receiver_phone:
            raise ValidationError("Please Define Receiver Phone Number")
        else:
            if '+' in receiver_id.phone:
                receiver_phone = receiver_id.phone.replace('+', '')

        # check sender Address
        if not sender_id.zip or not sender_id.city or not sender_id.country_id:
            raise ValidationError("Please Define Proper Sender Address!")

        # check Receiver Address
        if not receiver_id.zip or not receiver_id.city or not receiver_id.country_id:
            raise ValidationError("Please Define Proper Recipient Address!")
        master_node = etree.Element('soapenv:Envelope')
        master_node.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        master_node.attrib['xmlns:xsd'] = 'http://www.w3.org/2001/XMLSchema'
        master_node.attrib['xmlns:soapenv'] = 'http://schemas.xmlsoap.org/soap/envelope/'
        master_node.attrib['xmlns:est'] = 'http://estafetalabel.webservices.estafeta.com'
        etree.SubElement(master_node, 'soapenv:Header')
        submaster_node_body = etree.SubElement(master_node, 'soapenv:Body')
        submaster_node_createlable = etree.SubElement(submaster_node_body, 'est:createLabel')
        submaster_node_createlable.attrib['soapenv:encodingStyle'] = 'http://schemas.xmlsoap.org/soap/encoding/'
        submaster_node_in0 = etree.SubElement(submaster_node_createlable, 'in0')
        submaster_node_in0.attrib['xsi:type'] = 'dto:EstafetaLabelRequest'
        submaster_node_in0.attrib['xmlns:dto'] = 'http://dto.estafetalabel.webservices.estafeta.com'
        etree.SubElement(submaster_node_in0, 'customerNumber').text = "{}".format(
            picking.company_id and picking.company_id.estafeta_customer_number)
        root_node_labelDescriptionList = etree.SubElement(submaster_node_in0, 'labelDescriptionList')
        root_node_labelDescriptionList.attrib['xsi:type'] = 'dto:LabelDescriptionList'
        etree.SubElement(root_node_labelDescriptionList, 'content').text = '{}'.format(picking.name)
        etree.SubElement(root_node_labelDescriptionList, 'deliveryToEstafetaOffice').text = "{}".format(
            self.deliver_to_estafeta_office)
        sub_root_node_destinationInfo = etree.SubElement(root_node_labelDescriptionList, 'destinationInfo')
        sub_root_node_destinationInfo.attrib['xsi:type'] = 'dto:DestinationInfo'
        etree.SubElement(sub_root_node_destinationInfo, 'address1').text = "{}".format(receiver_id.street)
        etree.SubElement(sub_root_node_destinationInfo, 'city').text = "{}".format(receiver_id and receiver_id.city)
        etree.SubElement(sub_root_node_destinationInfo, 'contactName').text = "{}".format(receiver_id.name)
        etree.SubElement(sub_root_node_destinationInfo, 'corporateName').text = "{}".format(receiver_id.name)
        etree.SubElement(sub_root_node_destinationInfo, 'phoneNumber').text = "{}".format(receiver_phone)
        etree.SubElement(sub_root_node_destinationInfo, 'neighborhood').text = "{}".format(receiver_id.name)
        etree.SubElement(sub_root_node_destinationInfo, 'state').text = "{}".format(
            receiver_id.state_id and receiver_id.state_id.name)
        etree.SubElement(sub_root_node_destinationInfo, 'valid').text = "True"
        etree.SubElement(sub_root_node_destinationInfo, 'zipCode').text = "{}".format(receiver_id.zip)
        etree.SubElement(root_node_labelDescriptionList, 'numberOfLabels').text = "{}".format(
            picking.estafeta_number_of_labels if self.service_code == "79" else "1")
        etree.SubElement(root_node_labelDescriptionList, 'officeNum').text = "{}".format(office_number)
        sub_root_node_originInfo = etree.SubElement(root_node_labelDescriptionList, 'originInfo')
        sub_root_node_originInfo.attrib['xsi:type'] = 'dto:OriginInfo'
        etree.SubElement(sub_root_node_originInfo, 'address1').text = "{}".format(sender_id.street)
        etree.SubElement(sub_root_node_originInfo, 'city').text = "{}".format(sender_id.city)
        etree.SubElement(sub_root_node_originInfo, 'contactName').text = "{}".format(sender_id.name)
        etree.SubElement(sub_root_node_originInfo, 'corporateName').text = "{}".format(sender_id.name)
        etree.SubElement(sub_root_node_originInfo, 'customerNumber').text = "{}".format(
            sender_id.estafeta_customer_number)
        etree.SubElement(sub_root_node_originInfo, 'neighborhood').text = "{}".format(sender_id.name)
        etree.SubElement(sub_root_node_originInfo, 'phoneNumber').text = "{}".format(sender_phone)
        etree.SubElement(sub_root_node_originInfo, 'state').text = "{}".format(
            sender_id.state_id and sender_id.state_id.name)
        etree.SubElement(sub_root_node_originInfo, 'valid').text = "True"
        etree.SubElement(sub_root_node_originInfo, 'zipCode').text = "{}".format(sender_id.zip)
        etree.SubElement(root_node_labelDescriptionList, 'originZipCodeForRouting').text = "{}".format(sender_id.zip)
        etree.SubElement(root_node_labelDescriptionList, 'parcelTypeId').text = "{}".format(
            self.estafeat_parcel_type_id)
        etree.SubElement(root_node_labelDescriptionList, 'returnDocument').text = "{}".format(
            self.estafeat_return_documnet)
        etree.SubElement(root_node_labelDescriptionList, 'serviceTypeId').text = "{}".format(self.service_code)
        etree.SubElement(root_node_labelDescriptionList, 'valid').text = "True"
        etree.SubElement(root_node_labelDescriptionList, 'weight').text = "{}".format(picking.shipping_weight)
        etree.SubElement(submaster_node_in0, 'labelDescriptionListCount').text = "1"
        etree.SubElement(submaster_node_in0, 'login').text = '{}'.format(self.company_id.estafeta_username)
        etree.SubElement(submaster_node_in0, 'paperType').text = "{}".format(self.estafeta_paper_type)
        etree.SubElement(submaster_node_in0, 'password').text = "{}".format(self.company_id.estafeta_password)
        etree.SubElement(submaster_node_in0, 'suscriberId').text = "{}".format(self.company_id.estafeta_suscriberId)
        etree.SubElement(submaster_node_in0, 'quadrant').text = "1"
        etree.SubElement(submaster_node_in0, 'valid').text = "True"
        return etree.tostring(master_node)

    @api.model
    def estafeta_send_shipping(self, pickings):
        try:
            request_data = self.estafeta_label_request_data(pickings)
            _logger.info(request_data)
            url = "{}".format(self.company_id and self.company_id.estafeta_api_url)
            headers = {
                "SOAPAction": "",
                "Content-Type": "text/xml; charset=utf-8"
            }
            response = requests.post(url=url, data=request_data, headers=headers)
            _logger.info("Sending Post Request To {}".format(url))
            if response.status_code != 200:
                raise ValidationError(("Label Request Data Invalid! %s ") % (response.content))
            response_data = Response(response)
            result = response_data.dict()
            _logger.info("Estafet Response Data {}".format(result))
            label_data = result.get('Envelope').get('Body').get('multiRef')[0].get('labelPDF').get('value')
            if label_data == None:
                error_message = self.custom_error_message(error_message=result)
                if error_message:
                    error_message = (', \n'.join(error_message))
                raise ValidationError(_(error_message or result))
            tracking_number = result.get('Envelope').get('Body').get('multiRef')[1].get('resultDescription').get(
                'value')
            # spanish_tracking_number= result.get('Envelope').get('Body').get('multiRef')[2].get('resultSpanishDescription').get('value')
            if not label_data:
                _logger.info("Label Not Found Response")
            else:
                binary_data = binascii.a2b_base64(str(label_data))
                message = (("Label created!<br/> <b>Label Tracking Number : </b>%s<br/> <b>") % (tracking_number))
                pickings.message_post(body=message, attachments=[
                    ('Label-%s.%s' % (tracking_number, "pdf"), binary_data)])
                pickings.carrier_tracking_ref = tracking_number
                shipping_data = {
                    'exact_price': 0.0,
                    'tracking_number': tracking_number}
                response = [shipping_data]
                return response
        except Exception as e:
            raise ValidationError(e)

    def estafeta_traking_data(self, pickings=False):
        """ this method return body data  of tracking request """

        master_node = etree.Element('Envelope')
        master_node.attrib['xmlns'] = "http://schemas.xmlsoap.org/soap/envelope/"
        sub_master_node_body = etree.SubElement(master_node, 'Body')
        sub_master_node_ExecuteQuery = etree.SubElement(sub_master_node_body, 'ExecuteQuery')
        sub_master_node_ExecuteQuery.attrib['xmlns'] = "http://www.estafeta.com/"
        etree.SubElement(sub_master_node_ExecuteQuery, 'suscriberId').text = "{}".format(
            self.company_id.estafeta_suscriberId)
        etree.SubElement(sub_master_node_ExecuteQuery, 'login').text = "{}".format(self.company_id.estafeta_username)
        etree.SubElement(sub_master_node_ExecuteQuery, 'password').text = "{}".format(self.company_id.estafeta_password)
        root_node_searchType = etree.SubElement(sub_master_node_ExecuteQuery, "searchType")
        sub_root_node_waybillList = etree.SubElement(root_node_searchType, 'waybillList')
        etree.SubElement(sub_root_node_waybillList, 'waybillType').text = "{}".format('G')
        sub_root_node_waybills = etree.SubElement(sub_root_node_waybillList, 'waybills')
        etree.SubElement(sub_root_node_waybills, 'string').text = "{}".format(pickings.carrier_tracking_ref)
        etree.SubElement(root_node_searchType, 'type').text = "{}".format("L")
        sub_root_node_searchConfiguration = etree.SubElement(sub_master_node_ExecuteQuery, 'searchConfiguration')
        etree.SubElement(sub_root_node_searchConfiguration, 'includeDimensions').text = "{}".format(1)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeWaybillReplaceData').text = "{}".format(0)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeReturnDocumentData').text = "{}".format(0)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeMultipleServiceData').text = "{}".format(0)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeInternationalData').text = "{}".format(0)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeSignature').text = "{}".format(0)
        etree.SubElement(sub_root_node_searchConfiguration, 'includeCustomerInfo').text = "{}".format(1)
        sub_root_node_historyConfiguration = etree.SubElement(sub_root_node_searchConfiguration, 'historyConfiguration')
        etree.SubElement(sub_root_node_historyConfiguration, 'includeHistory').text = "{}".format(1)
        etree.SubElement(sub_root_node_historyConfiguration, 'historyType').text = "{}".format("ALL")
        sub_root_node_filterType = etree.SubElement(sub_root_node_searchConfiguration, 'filterType')
        etree.SubElement(sub_root_node_filterType, 'filterInformation').text = "{}".format(0)
        return etree.tostring(master_node)

    def estafeta_cancel_shipment(self, pickings):
        raise ValidationError(_('Estafeta Not Provide Cancel Service '))

    def estafeta_get_tracking_link(self, pickings):
        api_url = "https://trackingqa.estafeta.com/Service.asmx"
        headers = {
            "SOAPAction": "http://www.estafeta.com/ExecuteQuery",
            "Content-Type": "text/xml; charset=utf-8"}
        request_data = self.estafeta_traking_data(pickings)
        try:
            response_data = requests.post(url=api_url, data=request_data, headers=headers)
            if response_data.status_code in [200, 201]:
                _logger.info("Get Successfully Response From {}".format(api_url))
                response_data = Response(response_data)
                result = response_data.dict()
                parcel_status = result.get('Envelope') and result.get('Envelope').get('Body') and result.get(
                    'Envelope').get('Body').get('ExecuteQueryResponse') and result.get('Envelope').get('Body').get(
                    'ExecuteQueryResponse').get('ExecuteQueryResult') and result.get('Envelope').get('Body').get(
                    'ExecuteQueryResponse').get('ExecuteQueryResult').get('trackingData') and result.get(
                    'Envelope').get('Body').get('ExecuteQueryResponse').get('ExecuteQueryResult').get(
                    'trackingData').get('TrackingData') and result.get('Envelope').get('Body').get(
                    'ExecuteQueryResponse').get('ExecuteQueryResult').get('trackingData').get('TrackingData').get(
                    'statusENG')
                # delivery_data = result.get('Envelope').get('Body').get('ExecuteQueryResponse').get(
                #     'ExecuteQueryResult').get('trackingData').get('TrackingData').get('deliveryData')
                if not parcel_status:
                    raise ValidationError("estafeta parcel status not found in resonse {}".format(result))
                else:
                    pickings.write({'estafeta_parcel_status': "{0}".format(parcel_status)})
                return "https://www.estafeta.com/Tracking"
            else:
                raise ValidationError(response_data)
        except Exception as e:
            raise ValidationError(e)

    def custom_error_message(self, error_message):
        messages = error_message.get('Envelope') and error_message.get('Envelope').get('Body') and error_message.get(
            'Envelope').get('Body').get('multiRef')
        msg_list = []
        if messages:
            for msg in messages:
                value = msg and msg.get('resultDescription') and msg.get('resultDescription').get('value')
                if value:
                    msg_list.append(value)
            return msg_list
        else:
            return False
