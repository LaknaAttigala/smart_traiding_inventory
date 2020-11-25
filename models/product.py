# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models


class CustomProductsField(models.Model):
  _inherit = 'product.template'

  list_price = fields.Float(string='Minimim Sale Price')
  cus_product_id = fields.Char('Product ID')
  box_quantity = fields.Float('Quantity Per Box', default=1)
  cus_length = fields.Float('Length', store=True)
  cus_width = fields.Float('Width', store=True)
    
  