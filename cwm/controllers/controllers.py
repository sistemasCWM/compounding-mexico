# -*- coding: utf-8 -*-
# from odoo import http


# class Cwm(http.Controller):
#     @http.route('/cwm/cwm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cwm/cwm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cwm.listing', {
#             'root': '/cwm/cwm',
#             'objects': http.request.env['cwm.cwm'].search([]),
#         })

#     @http.route('/cwm/cwm/objects/<model("cwm.cwm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cwm.object', {
#             'object': obj
#         })
