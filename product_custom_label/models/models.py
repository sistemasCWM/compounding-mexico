# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api
from odoo.addons.base.models.report_paperformat import PAPER_SIZES


class PrintFormatTemplate(models.Model):
    _name = 'print.format.template'
    _rec_name = 'template_name'

    logo = fields.Image()
    logo_height = fields.Integer(string='Logo Height(px)')
    logo_width = fields.Integer(string='Logo Width(px)')
    template_name = fields.Char(required=True)
    is_default = fields.Boolean()
    print_lot_seq = fields.Boolean()
    print_lot_barcode = fields.Boolean()

    is_preview = fields.Boolean()

    preview = fields.Binary()
    human_readability = fields.Boolean()
    barcode_quiet = fields.Boolean(help='Remove extra white space from left & right of barcode')
    template_for = fields.Selection([('product.template', 'Product Template'), ('product.product', 'Product Variant')],
                                    required=True)
    orientation = fields.Selection([('Portrait', 'Portrait'), ('Landscape', 'Landscape')], default='Portrait')
    format = fields.Selection([(ps['key'], ps['description']) for ps in PAPER_SIZES], 'Paper size', default='A4',
                              help="Select Proper Paper size")
    quantity = fields.Integer(default=1, string='#Of Prints')
    page_height = fields.Integer(string='Paper Height(mm)')
    page_width = fields.Integer(string='Paper Width(mm)')
    barcode_height = fields.Integer(string='Barcode Height(px)')
    barcode_width = fields.Integer(string='Barcode Width(px)')
    barcode_type = fields.Selection([
        ('Codabar', 'Codabar'),
        ('Code11', 'Code11'),
        ('Code128', 'Code128'),
        ('EAN13', 'EAN13'),
        ('EAN8', 'EAN8'),
        ('Extended39', 'Extended39'),
        ('Extended93', 'Extended93'),
        ('FIM', 'FIM'),
        ('I2of5', 'I2of5'),
        ('MSI', 'MSI'),
        ('POSTNET', 'POSTNET'),
        ('Standard39', 'Standard39'),
        ('Standard93', 'Standard93'),
        ('UPCA', 'UPCA'),
        ('USPS_4State', 'USPS_4State'),
        ('QR', 'QR'),

    ], 'Barcode Type', default='EAN13', required=True, )
    field_line_ids = fields.One2many('field.line', 'format_template', string='Field Lines')
    label_align = fields.Selection([('left', 'Left'), ('center', 'Center'), ('Right', 'Right')], string='Content Align',
                                   default='center')
    lot_font = fields.Integer()
    is_print_lot = fields.Boolean()
    lot_color = fields.Char(default='#000000')

    @api.onchange('barcode_type', 'barcode_height', 'barcode_width')
    def qr_shape(self):
        if self.barcode_type == 'QR':
            self.barcode_height = self.barcode_width

    def generate_report_file(self):
        paper_format = self.env['ir.model.data'].xmlid_to_object(
            'product_custom_label.product_custom_label_preview_paperformat')
        paper_format.page_height = False
        paper_format.page_width = False
        paper_format.format = self.format
        paper_format.orientation = self.orientation
        if self.format == 'custom':
            paper_format.page_height = self.page_height
            paper_format.page_width = self.page_width
            paper_format.margin_top = 5
            paper_format.margin_bottom = 5
        pdf = self.env.ref('product_custom_label.product_custom_label_print_preview_report')._render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        self.preview = b64_pdf


class FieldLine(models.Model):
    _name = 'field.line'
    _rec_name = 'field_name'
    _order = 'sequence asc'

    sequence = fields.Integer()
    field_name = fields.Many2one('ir.model.fields')
    font_size = fields.Integer(required=True, default=15)
    bold = fields.Boolean()
    italic = fields.Boolean()
    underline = fields.Boolean()
    color = fields.Char(default='#000000')
    format_template = fields.Many2one('print.format.template')
