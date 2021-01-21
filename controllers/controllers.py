# -*- coding: utf-8 -*-
from flectra import http

# class SmartTraidingInventory(http.Controller):
#     @http.route('/smart_traiding_inventory/smart_traiding_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_traiding_inventory/smart_traiding_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_traiding_inventory.listing', {
#             'root': '/smart_traiding_inventory/smart_traiding_inventory',
#             'objects': http.request.env['smart_traiding_inventory.smart_traiding_inventory'].search([]),
#         })

#     @http.route('/smart_traiding_inventory/smart_traiding_inventory/objects/<model("smart_traiding_inventory.smart_traiding_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_traiding_inventory.object', {
#             'object': obj
#         })