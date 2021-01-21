# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models


class PurchaseOrederCancelReason(models.Model):
  _name = 'smart_traiding_inventory.purchaseordercancelreson'

  name = fields.Text('Reason', required=True, translate=True)
  

  @api.multi
  def purchase_order_cancel_reason_apply(self):
    leads = self.env['purchase.order'].browse(self.env.context.get('active_ids'))
    leads.write({'cancel_order_reason': self.name})
    return leads.write({'state': 'cancel'})
    # leads = self.env['hr.holidays'].browse(self.env.context.get('active_ids'))
    # leads.write({'cancellevesreason': self.cancellevesreason.id})
    # return leads.action_refuse()

