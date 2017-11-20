# -*- coding: utf-8 -*-
from odoo import http

# class AlltopDeletedemodata(http.Controller):
#     @http.route('/alltop_deletedemodata/alltop_deletedemodata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alltop_deletedemodata/alltop_deletedemodata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alltop_deletedemodata.listing', {
#             'root': '/alltop_deletedemodata/alltop_deletedemodata',
#             'objects': http.request.env['alltop_deletedemodata.alltop_deletedemodata'].search([]),
#         })

#     @http.route('/alltop_deletedemodata/alltop_deletedemodata/objects/<model("alltop_deletedemodata.alltop_deletedemodata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alltop_deletedemodata.object', {
#             'object': obj
#         })