# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models


class Partner(models.Model):
  _inherit = 'res.partner'
    
  vat2= fields.Char("VAT")
  svat = fields.Char("SVAT")
  br_number = fields.Char("BR Number")


  @api.model
  def create(self, vals):
    res = super(Partner,self).create(vals)
    if res.customer:
      res.write({'active': False})
    return res