from odoo import models, fields, api
from odoo.addons.base.models.report_paperformat import PAPER_SIZES


class CustomLabelWizard(models.TransientModel):
    _name = 'product.custom.label.wizard'

    template_id = fields.Many2one('print.format.template', required=True)
    edit_template = fields.Boolean()
    logo = fields.Image()
    logo_height = fields.Integer(string='Logo Height(px)')
    logo_width = fields.Integer(string='Logo Width(px)')
    template_name = fields.Char()
    is_default = fields.Boolean()
    human_readability = fields.Boolean()
    barcode_quiet = fields.Boolean(help='Remove extra white space from left & right of barcode')
    template_for = fields.Selection([('product.product', 'Product Template'), ('product.template', 'Product Variant')],
                                    required=True)
    quantity = fields.Integer(default=1, string='#Of Prints')
    currency_id = fields.Many2one('res.currency')
    orientation = fields.Selection([('Portrait', 'Portrait'), ('Landscape', 'Landscape')], default='Portrait')
    format = fields.Selection([(ps['key'], ps['description']) for ps in PAPER_SIZES], 'Paper size', default='A4',
                              help="Select Proper Paper size")
    page_height = fields.Integer(string='Paper Height(mm)')
    page_width = fields.Integer(string='Paper Width(mm)')
    barcode_height = fields.Integer(string='Barcode Height(px)')
    barcode_width = fields.Integer(string='Barcode Width(px)')
    product_active_ids = fields.Many2many('product.product')
    template_active_ids = fields.Many2many('product.template')
    field_line_tran_ids = fields.One2many('field.line.wizard', 'format_temp_wizard', string='Field Lines')
    label_align = fields.Selection([('left', 'Left'), ('center', 'Center'), ('Right', 'Right')], string='Content Align')
    lot_font = fields.Integer()
    lot_color = fields.Char(default='#000000')
    product_variant_lot_ids = fields.One2many('lot.lines', 'product_variant_custom_label_id',
                                              string="Product Variant Lot")
    product_template_lot_ids = fields.One2many('lot.lines', 'product_template_custom_label_id',
                                               string="Product Template Lot")
    print_lot_seq = fields.Boolean()
    print_lot_barcode = fields.Boolean()
    is_print_lot = fields.Boolean()
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

    ], 'Barcode Type', default='Codabar', required=True)

    @api.onchange('barcode_type', 'barcode_height', 'barcode_width')
    def qr_shape(self):
        if self.barcode_type == 'QR':
            self.barcode_height = self.barcode_width

    def product_print_label(self):
        paper_format = self.env['ir.model.data'].xmlid_to_object('product_custom_label.product_custom_label_paperformat')
        paper_format.page_height = False
        paper_format.page_width = False
        paper_format.format = self.format

        paper_format.orientation = self.orientation
        if self.format == 'custom':
            paper_format.page_height = self.page_height
            paper_format.page_width = self.page_width
        return self.env.ref('product_custom_label.product_custom_label_report').report_action(self, {})

    def template_print_label(self):
        paper_format = self.env['ir.model.data'].xmlid_to_object('product_custom_label.product_custom_label_paperformat')
        paper_format.page_height = False
        paper_format.page_width = False
        paper_format.format = self.format

        paper_format.orientation = self.orientation
        if self.format == 'custom':
            paper_format.page_height = self.page_height
            paper_format.page_width = self.page_width
            paper_format.margin_top = 5
            paper_format.margin_bottom = 5
        return self.env.ref('product_custom_label.template_custom_label_report').report_action(self, {})

    @api.onchange('template_id')
    def fill_data(self):
        ls = []
        self.is_default = self.template_id.is_default
        self.human_readability = self.template_id.human_readability
        self.logo = self.template_id.logo
        self.logo_height = self.template_id.logo_height
        self.logo_width = self.template_id.logo_width
        self.template_for = self.template_id.template_for
        self.quantity = self.template_id.quantity
        self.orientation = self.template_id.orientation
        self.format = self.template_id.format
        self.page_height = self.template_id.page_height
        self.page_width = self.template_id.page_width
        self.barcode_height = self.template_id.barcode_height
        self.barcode_width = self.template_id.barcode_width
        self.label_align = self.template_id.label_align
        self.barcode_quiet = self.template_id.barcode_quiet
        self.is_print_lot = self.template_id.is_print_lot
        self.lot_font = self.template_id.lot_font
        self.lot_color = self.template_id.lot_color
        self.print_lot_seq = self.template_id.print_lot_seq
        self.print_lot_barcode = self.template_id.print_lot_barcode
        for field_line_id in self.template_id.field_line_ids:
            ls.append(
                [0, 0, {
                    'field_name': field_line_id.field_name.id,
                    'color': field_line_id.color,
                    'font_size': field_line_id.font_size,
                    'bold': field_line_id.bold,
                    'italic': field_line_id.italic,
                    'underline': field_line_id.underline,
                }]
            )
        self.field_line_tran_ids = False
        self.field_line_tran_ids = ls

    @api.onchange('product_active_ids')
    def add_lots_for_extra_product_ver(self):
        rec = {}
        if self.product_active_ids and not self.product_variant_lot_ids:
            items = []
            for active_id in self.product_active_ids:
                items.append((0, 0, {'product_variant_id': active_id.id}))

            rec['product_variant_lot_ids'] = items
            self.update(rec)
        else:
            to_remove = []
            current_product_in = []

            for lot_product_id in self.product_variant_lot_ids:
                if lot_product_id.product_variant_id.id not in self.product_active_ids.ids:
                    to_remove.append((2, lot_product_id.id))
                else:
                    current_product_in.append(lot_product_id.product_variant_id.id)
            rec['product_variant_lot_ids'] = to_remove
            self.update(rec)
            to_add = []
            for product_id in self.product_active_ids:
                if product_id.ids[0] not in current_product_in:
                    to_add.append((0, 0, {'product_variant_id': product_id.ids[0]}))
            rec['product_variant_lot_ids'] = to_add
            self.update(rec)

    @api.onchange('template_active_ids')
    def add_lots_for_extra_product_tmp(self):
        rec = {}
        if self.template_active_ids and not self.product_template_lot_ids:
            items = []
            for active_id in self.template_active_ids:
                items.append((0, 0, {'product_template_id': active_id.id}))
            rec['product_template_lot_ids'] = items
            self.update(rec)
        else:
            to_remove = []
            current_product_in = []

            for lot_product_id in self.product_template_lot_ids:
                if lot_product_id.product_template_id.id not in self.template_active_ids.ids:
                    to_remove.append((2, lot_product_id.id))
                else:
                    current_product_in.append(lot_product_id.product_template_id.id)
            rec['product_template_lot_ids'] = to_remove
            self.update(rec)
            to_add = []
            for product_id in self.template_active_ids:
                if product_id.ids[0] not in current_product_in:
                    to_add.append((0, 0, {'product_template_id': product_id.ids[0]}))
            rec['product_template_lot_ids'] = to_add
            self.update(rec)


class LotLines(models.TransientModel):
    _name = 'lot.lines'

    product_variant_id = fields.Many2one('product.product')
    product_template_id = fields.Many2one('product.template')
    product_lot_ids = fields.Many2many('stock.production.lot')
    product_variant_custom_label_id = fields.Many2one('product.custom.label.wizard')
    product_template_custom_label_id = fields.Many2one('product.custom.label.wizard')


class FieldLineWizard(models.TransientModel):
    _name = 'field.line.wizard'
    _order = 'sequence asc'

    sequence = fields.Integer()
    field_name = fields.Many2one('ir.model.fields')
    font_size = fields.Integer(default=15, required=True)
    bold = fields.Boolean()
    italic = fields.Boolean()
    underline = fields.Boolean()
    color = fields.Char(default='#000000')
    format_temp_wizard = fields.Many2one('product.custom.label.wizard')


class ProductWizard(models.Model):
    _inherit = 'product.product'

    def open_custom_label_wizard(self):

        default_template_id = self.env['print.format.template'].search(
            [('is_default', '=', True), ('template_for', '=', 'product.product')],
            limit=1)

        if not default_template_id:
            default_template_id = self.env['print.format.template'].search(
                [('template_for', '=', 'product.template')], limit=1)

        rec = self.env['product.custom.label.wizard'].create({
            'template_id': default_template_id.id,
            'template_for': default_template_id.template_for,
            'currency_id': self.env.company.currency_id.id,
            'product_active_ids': self.env.context.get('active_ids', False),
        })
        rec.fill_data()
        rec.add_lots_for_extra_product_ver()

        return {
            'name': 'Custom Label Wizard',
            'res_model': 'product.custom.label.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'current_model': self.env.context.get('active_model', False),
            },
            'res_id': rec.id,
            'type': 'ir.actions.act_window'
        }

    def get_field_value(self, field_id):
        value = ""
        if field_id and field_id.model_id.model == 'product.product':

            if field_id.ttype in ['one2many', 'many2many']:
                value = ''
            elif field_id.ttype == 'many2one':
                value = self[field_id.name].display_name
            else:
                value = self[field_id.name]
        return value


class TemplateWizard(models.Model):
    _inherit = 'product.template'

    def open_custom_label_wizard(self):
        default_template_id = self.env['print.format.template'].search(
            [('is_default', '=', True), ('template_for', '=', 'product.template')], limit=1)
        if not default_template_id:
            default_template_id = self.env['print.format.template'].search(
                [('template_for', '=', 'product.template')], limit=1)
        rec = self.env['product.custom.label.wizard'].create({
            'template_id': default_template_id.id,
            'template_for': default_template_id.template_for,
            'currency_id': self.env.company.currency_id.id,
            'template_active_ids': self.env.context.get('active_ids', False),
        })
        rec.fill_data()
        rec.add_lots_for_extra_product_tmp()
        return {
            'name': 'Custom Label Wizard',
            'res_model': 'product.custom.label.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'current_model': self.env.context.get('active_model', False),
            },
            'res_id': rec.id,
            'type': 'ir.actions.act_window'
        }

    def get_field_value(self, field_id):
        value = ''
        if field_id and field_id.model_id.model == 'product.template':
            if field_id.ttype in ['one2many', 'many2many']:
                value = ''
            elif field_id.ttype == 'many2one':
                value = self[field_id.name].display_name
            else:
                value = self[field_id.name]
        return value
