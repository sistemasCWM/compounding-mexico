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
    """
    # kpi_quote = fields.Boolean('Confirmed Sales by Salesperson')
    kpi_quote = fields.Boolean('Confirmed Sales')
    kpi_quote_value = fields.Integer(compute="_compute_kpi_quote_value")

    def _compute_kpi_quote_value(self):
        # self.kpi_quote_value = 123
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            quote = self.env['sale.order'].search_count([('state', '=', 'sent'), ('date_order', '>=', start), ('date_order', '<', end)])
            record.kpi_quote_value = quote

    """
    2) Feature 2
    KPI no. 2
        Confirmed sales of new clients
            Show an aggregate of all the confirmed sales from new clients
    """
    # kpi_newclient = fields.Boolean(compute="_compute_kpi_newclient_value"),def _compute_kpi_newclient_value()(self):,print('456')

    # kpi_new_client = fields.Boolean('Confirmed sales of new clients')
    kpi_new_client = fields.Boolean('Confirmed New Sales')
    kpi_new_client_value = fields.Integer(compute="_compute_kpi_new_client_value")

    def _compute_kpi_new_client_value(self):
        
        # self.kpi_new_client_value = 456

        start_datetime = datetime.utcnow() + relativedelta(days=-1)
        end_datetime = datetime.utcnow() + relativedelta(days=+1)

        client_ids = self.env['res.partner'].search_count([('create_date', '>=', start_datetime), ('create_date', '<=', end_datetime)])

        # print(type(client_ids))

        # if type(client_ids) == "<class 'int'>":
        if type(client_ids) == int:
            client_ids = [client_ids]

        # print(client_ids)

        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            new_client = self.env['sale.order'].search_count([('state', '=', 'sent'), ('date_order', '>=', start), ('date_order', '<', end), ('partner_id', 'in', client_ids)])
            # print(new_client)
            # print(new_client)
            record.kpi_new_client_value = new_client
    
    """
    3) Feature 3
    KPI no.3
    Bank account balance in General Ledger
        Show the balance in General Ledger for each bank account set up in the Accounting App.
        Be ready to include more accounts if they were to be added in the future
        Be ready to not show previous accounts if they get deleted.
    """

    # kpi_bank_account = fields.Boolean('Bank account balance in General Ledger')
    # kpi_bank_account_value = fields.Integer(compute="_compute_kpi_bank_account_value")

    def _compute_kpi_bank_account_value(self):
        
        """
        # self.kpi_bank_account_value = 789

        account_journal = account.account_journal()
        
        bank_account = account_journal.get_journal_dashboard_datas['account_balance']

        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            # bank_account = self.env['sale.order'].search_count([('state', '=', 'sent'), ('date_order', '>=', start), ('date_order', '<', end)])
            record.kpi_bank_account_value =
        """
        
        # print(self)
        balances = []

        accounts = self.env['account.journal'].search([['type', '=', 'bank']])

        for account in accounts:
        
            balances.append([
                account.name,
                account._get_journal_bank_account_balance()[0]
            ])
        
        # print(balances)
        

        # self.kpi_bank_account_value = 789

        return balances

    def _action_send_to_user(self, user, tips_count=1, consum_tips=True):
        print('En el método >def _action_send_to_user(self, user, tips_count=1, consum_tips=True):< heredado')
        print(self._compute_kpi_bank_account_value())
        rendered_body = self.env['mail.render.mixin'].with_context(preserve_comments=True)._render_template(
            # 'digest.digest_mail_main',
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
                'bank_balances': self._compute_kpi_bank_account_value()
            },
            post_process=True
        )[self.id]
        print(rendered_body)
        full_mail = self.env['mail.render.mixin']._render_encapsulate(
            'digest.digest_mail_layout',
            rendered_body,
            add_context={
                'company': user.company_id,
                'user': user,
            },
        )
        # create a mail_mail based on values, without attachments
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