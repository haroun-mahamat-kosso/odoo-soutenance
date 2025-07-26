# -*- coding: utf-8 -*-
# from odoo import http


# class FormationSup(http.Controller):
#     @http.route('/formation__sup/formation__sup', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/formation__sup/formation__sup/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('formation__sup.listing', {
#             'root': '/formation__sup/formation__sup',
#             'objects': http.request.env['formation__sup.formation__sup'].search([]),
#         })

#     @http.route('/formation__sup/formation__sup/objects/<model("formation__sup.formation__sup"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('formation__sup.object', {
#             'object': obj
#         })
