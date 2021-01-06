
#     partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.")
# _name = "purchase.order"

# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
from flectra import api, fields, models, SUPERUSER_ID, _
from flectra.exceptions import UserError, AccessError, ValidationError
from flectra.tools.float_utils import float_compare
from flectra.addons import decimal_precision as dp
from datetime import datetime


class CustomerPurchaseFields(models.Model):
  _inherit = "purchase.order"


  cus_others = fields.Char("Remarks")
  cancel_order_reason = fields.Text(string='Cancel Reason', index=True)
  cus_delivery_to = fields.Char(string='Delivery To', index=True)
 
  cus_approved = fields.Many2one('res.users', string="PQ Approved By", readonly=True, store=True)
  cus_approved_date = fields.Datetime(string="PQ Approved Date", readonly=True)


  state = fields.Selection([
    ('draft', 'New'),
    ('sent', 'RFQ Sent'),
    ('to approve', 'To Approve'),
    ('purchase', 'Purchase Order'),
    ('done', 'Locked'),
    ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
  
  
  @api.multi
  def approve_rfq(self):
    self.ensure_one()
    now_date = datetime.now()
    self.write({'cus_approved_date':now_date, 'cus_approved':self.env.user.id, 'state': 'sent'})
    return {}
  
  @api.multi
  def cus_cancel_button(self):
    for order in self:
      for pick in order.picking_ids:
        if pick.state == 'done':
          raise UserError(_('Unable to cancel purchase order %s as some receptions have already been done.') % (order.name))
      for inv in order.invoice_ids:
        if inv and inv.state not in ('cancel', 'draft'):
          raise UserError(_("Unable to cancel this purchase order. You must first cancel related vendor bills."))

            # If the product is MTO, change the procure_method of the the closest move to purchase to MTS.
            # The purpose is to link the po that the user will manually generate to the existing moves's chain.
      if order.state in ('draft', 'sent', 'to approve'):
        for order_line in order.order_line:
          if order_line.move_dest_ids:
            move_dest_ids = order_line.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))
            siblings_states = (move_dest_ids.mapped('move_orig_ids')).mapped('state')
            if all(state in ('done', 'cancel') for state in siblings_states):
              move_dest_ids.write({'procure_method': 'make_to_stock'})
              move_dest_ids._recompute_state()

      for pick in order.picking_ids.filtered(lambda r: r.state != 'cancel'):
        pick.action_cancel()

      order.order_line.write({'move_dest_ids':[(5,0,0)]})
    # return {
    #   'type': 'ir.actions.act_window',
    #   'tag': 'smart_traiding_inventory.purchase_order_cancel_reason_action',
    #   'target': 'New'
    # }
    return {
      'type': 'ir.actions.act_window',
      'name': 'Action Name',
      'target': 'new', #use 'current' for not opening in a dialog
      'res_model': 'smart_traiding_inventory.purchaseordercancelreson',
      'view_id': 'purchase_order_cancel_reason_view_form',#optional
      'view_type': 'form',
      'views': [[False,'form']],
    }
    # self.write({'state': 'cancel'})




  @api.multi
  def button_create_rfq(self):
    for order in self:
      if order.state not in ['accept purchase']:
        continue
      order.write({'state': 'draft'})
    return True

  @api.multi
  def button_creat_pr(self):
    for order in self:
      if order.state not in ['sent']:
        continue
      order.write({'state': 'request purchase'})
    return True
  
  @api.multi
  def button_or_approve(self):
    
    for order in self:
      if order.state not in ['request purchase']:
        continue
      if order.user_has_groups('purchase.group_purchase_manager'):
        order.write({'cus_approved':self.env.user.id})
        now_date = datetime.now()
        order.write({'cus_approved_date':now_date  })
        print("hgbffffffffffffffffhsadgfvdsyafudstfva",self.env.user)
        order.write({'state': 'accept purchase'})
      
    return True
  
  
  @api.multi
  def cus_button_order_confirm(self):
    for order in self:
      if order.state not in ['accept purchase']:
        continue
      order._add_supplier_to_product()
            # Deal with double validation process
      if order.company_id.po_double_validation == 'one_step'\
          or (order.company_id.po_double_validation == 'two_step'\
            and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
          or order.user_has_groups('purchase.group_purchase_manager'):
        order.button_approve()
      else:
        order.write({'state': 'to approve'})
    return True

