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

class Digest(models.Model):

    _inherit = 'digest.digest'

    inherit_test = fields.Char(string='Inherit Test', required=False, translate=True)

    kpi_quote = fields.Boolean('Confirmed sales')
    kpi_quote_value = fields.Integer(compute="_compute_kpi_quote_value")

    def _compute_kpi_quote_value(self):
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            quote = self.env['sale.order'].search_count([('state', '=', 'sale'), ('date_order', '>=', start), ('date_order', '<', end)])
            record.kpi_quote_value = quote

    kpi_new_client = fields.Boolean('Confirmed sales of new clients')
    kpi_new_client_value = fields.Integer(compute="_compute_kpi_new_client_value")

    def _compute_kpi_new_client_value(self):

        start_datetime = fields.Datetime.to_string(self._context.get('start_datetime') + relativedelta(days=-1))
        end_datetime = fields.Datetime.to_string(self._context.get('end_datetime') + relativedelta(days=+1))
        clients = self.env['res.partner'].search([('create_date', '>=', start_datetime), ('create_date', '<=', end_datetime)])
        client_ids = []

        for client in clients:
            client_ids.append(client.id)

        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            new_client = self.env['sale.order'].search_count([('state', '=', 'sale'), ('partner_id', 'in', client_ids)])
            record.kpi_new_client_value = new_client

    def _compute_kpi_bank_account_value(self):
        return [[x.name, '$' + "{0:,.2f}".format(x._get_journal_bank_account_balance()[0])] for x in self.env['account.journal'].search([['type', '=', 'bank']])]

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

    kpi_clients_with_no_sales = fields.Boolean('Clients with no sales')
    kpi_clients_with_no_sales_value = fields.Integer(compute="_compute_clients_with_no_sales")

    def _compute_clients_with_no_sales(self):

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

    kpi_clients_with_sales = fields.Boolean('Clients with sales')
    kpi_clients_with_sales_value = fields.Integer(compute="_compute_clients_with_sales")

    def _compute_clients_with_sales(self):

        start_datetime = fields.Datetime.to_string(self._context.get('start_datetime'))
        end_datetime = fields.Datetime.to_string(self._context.get('end_datetime'))
        clients = self.env['res.partner'].search([])
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
