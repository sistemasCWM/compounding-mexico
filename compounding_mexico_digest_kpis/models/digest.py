# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pytz

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from markupsafe import Markup

from odoo import api, fields, models, tools, _
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.exceptions import AccessError
from odoo.tools.float_utils import float_round

_logger = logging.getLogger(__name__)

# from odoo.addons import account

class Digest(models.Model):

    _inherit = 'digest.digest'

    inherit_test = fields.Char(string='Inherit Test', required=False, translate=True)
    
    """
    1) Feature 1
    KPI no. 1
        Confirmed Sales by Salesperson
            Showing a list with two columns. The column on the left contains the name of the salesperson and the column on the right total amount of his/her confirmed sales.

    2) Feature 2
    KPI no. 2
        Confirmed sales of new clients
            Show an aggregate of all the confirmed sales from new clients
    
    3) Feature 3
    KPI no.3
    Bank account balance in General Ledger
        Show the balance in General Ledger for each bank account set up in the Accounting App.
        Be ready to include more accounts if they were to be added in the future
        Be ready to not show previous accounts if they get deleted.
    """

    # KPI
    kpi_quote = fields.Boolean('Confirmed sales')
    kpi_quote_value = fields.Integer(compute="_compute_kpi_quote_value")

    def _compute_kpi_quote_value(self):
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            quote = self.env['sale.order'].search_count([('state', '=', 'sale'), ('date_order', '>=', start), ('date_order', '<', end)])
            record.kpi_quote_value = quote

    # KPI
    kpi_new_client = fields.Boolean('Confirmed sales to new clients')
    kpi_new_client_value = fields.Integer(compute="_compute_kpi_new_client_value")

    def _compute_kpi_new_client_value(self):

        start_datetime = fields.Datetime.to_string(self._context.get('start_datetime') + relativedelta(days=-1))
        end_datetime = fields.Datetime.to_string(self._context.get('end_datetime') + relativedelta(days=+1))
        client_ids = self.env['res.partner'].search_count([('create_date', '>=', start_datetime), ('create_date', '<=', end_datetime)])

        if type(client_ids) == int:
            client_ids = [client_ids]

        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            new_client = self.env['sale.order'].search_count([('state', '=', 'sale'), ('date_order', '>=', start), ('date_order', '<', end), ('partner_id', 'in', client_ids)])
            record.kpi_new_client_value = new_client

    # KPI
    def _compute_kpi_bank_account_value(self):
        return [[x.name, '$' + "{0:,.2f}".format(x._get_journal_bank_account_balance()[0])] for x in self.env['account.journal'].search([['type', '=', 'bank']])]

    # KPI
    def _compute_leaderboard_value(self, start):

        leaderboard = []
        salespeople = self.env['res.users'].search([['sale_team_id', '!=', False]])

        for salesperson in salespeople:
            leaderboard.append([
                salesperson.partner_id.name
                ,
                sum(sale_order.amount_total for sale_order in self.env['sale.order'].search([
                    ['user_id', '=', salesperson.id],
                    ['date_order', '>=', start],
                    ['date_order', '<=', datetime.now()],
                ]))
            ])
            leaderboard.sort(key=lambda x: x[1])
            leaderboard.reverse()

        for leader in leaderboard:
            leader[1] = '$' + "{0:,.2f}".format(leader[1])

        return leaderboard

    # KPI

    """
    1. Cliente que nunca haya comprado
    Este puede ser un cliente que sea totalmente nuevo o que ya se haya guardado su contacto pero nunca compró. 
    En este caso, si fueramos a poner esta info, se pondría también en la sección de clientes nuevos?
    """

    kpi_clients_with_no_sales = fields.Boolean('Clientes with no sales')
    kpi_clients_with_no_sales_value = fields.Integer(compute="_compute_clients_with_no_sales")

    def _compute_clients_with_no_sales(self):
        
        client_ids = []
        start_datetime = fields.Datetime.to_string(self._context.get('start_datetime'))
        end_datetime = fields.Datetime.to_string(self._context.get('end_datetime'))
        clients = self.env['res.partner'].search([])
        temporal = 0

        for client in clients:

            client_orders = self.env['sale.order'].search_count([('state', '=', 'sale'), ('date_order', '>=', start_datetime), ('date_order', '<', end_datetime), ('partner_id', 'in', [client.id])])

            if type(client_orders) == int:
                if client_orders == 0:
                    temporal += 1

        self.kpi_clients_with_no_sales_value = temporal

    # KPI

    """
    2. Cliente que ha sido registrado en el transcurso del mes
    Parece que sí se podría y ya su compra se reflejaría en la temporalidad que ya está definida en el reporte (1, 7 y 30 días). 
    """

    kpi_clients_with_sales = fields.Boolean('Clientes with sales')
    kpi_clients_with_sales_value = fields.Integer(compute="_compute_clients_with_sales")
    def _compute_clients_with_sales(self):

        start_datetime = fields.Datetime.to_string(self._context.get('start_datetime'))
        end_datetime = fields.Datetime.to_string(self._context.get('end_datetime'))
        clients = self.env['res.partner'].search([('create_date', '>=', start_datetime), ('create_date', '<=', end_datetime)])
        clients_amount = len(clients)
        temporal = 0

        for client in clients:
            client_orders = self.env['sale.order'].search_count([('state', '=', 'sale'), ('date_order', '>=', start_datetime), ('date_order', '<', end_datetime), ('partner_id', 'in', [client.id])])
            if type(client_orders) == int:
                if client_orders > 0:
                    temporal += 1
        
        self.kpi_clients_with_sales_value = temporal

    def _action_send_to_user(self, user, tips_count=1, consum_tips=True):
        rendered_body = self.env['mail.render.mixin'].with_context(preserve_comments=True)._render_template(
            'compounding_mexico_digest_kpis.digest_mail_main_compounding_mexico',
            'digest.digest',
            self.ids,
            engine='qweb_view',
            add_context={
                'title': self.name,
                'top_button_label': _('Connect'),
                'top_button_url': self.get_base_url(),
                'company': user.company_id,
                'user': user,
                'unsubscribe_token': self._get_unsubscribe_token(user.id),
                'tips_count': tips_count,
                'formatted_date': datetime.today().strftime('%B %d, %Y'),
                'display_mobile_banner': True,
                'kpi_data': self._compute_kpis(user.company_id, user),
                'tips': self._compute_tips(user.company_id, user, tips_count=tips_count, consumed=consum_tips),
                'preferences': self._compute_preferences(user.company_id, user),
                'bank_balances': self._compute_kpi_bank_account_value(),
                'leaderboard': self._compute_leaderboard_value(datetime.now() - relativedelta(days=1)),
                'leaderboard2': self._compute_leaderboard_value(datetime.now() - relativedelta(days=7)),
                'leaderboard3': self._compute_leaderboard_value(datetime.now() - relativedelta(days=30))
            },
            post_process=True
        )[self.id]
        full_mail = self.env['mail.render.mixin']._render_encapsulate(
            'digest.digest_mail_layout',
            rendered_body,
            add_context={
                'company': user.company_id,
                'user': user,
            },
        )
        mail_values = {
            'auto_delete': True,
            'author_id': self.env.user.partner_id.id,
            'email_from': (
                self.company_id.partner_id.email_formatted
                or self.env.user.email_formatted
                or self.env.ref('base.user_root').email_formatted
            ),
            'email_to': user.email_formatted,
            'body_html': full_mail,
            'state': 'outgoing',
            'subject': '%s: %s' % (user.company_id.name, self.name),
        }
        self.env['mail.mail'].sudo().create(mail_values)
        return True
