
#     partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.")
# _name = "purchase.order"

# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models


class CustomerPurchaseFields(models.Model):
  _inherit = "stock.picking"
    
  partner_id = fields.Many2one(string='Vendor')
  cus_paid = fields.Char(string='Paid',  default='None', readonly=True)
  origin = fields.Char( string="PO Number")
  cus_source= fields.Char("Source Document")

  
  # cus_package_qty = fields.Integer('Pack Qty', store=True)
  

  def select_do_print_picking(self):
    pick_return = self.origin
    pick_type = self.picking_type_code
    if pick_type=="incoming":
      if pick_return[:6] =="Return":
        self.write({'printed': True})
        return self.env.ref('smart_traiding_inventory.menu_action_report_purchase_return').report_action(self)
      else:
        self.write({'printed': True})
        return self.env.ref('smart_traiding_inventory.menu_action_report_grn_doc').report_action(self)
    elif pick_type =="outgoing":
      if pick_return[:6] =="Return":
        print("jakbsdjashjddsffffffffffffffffff outg",pick_return[:6])
      else:
        self.write({'printed': True})
        return self.env.ref('smart_traiding_inventory.menu_action_report_aod_doc').report_action(self)
    else:
      self.write({'printed': True})
      return self.env.ref('stock.action_report_picking').report_action(self)
    # self.write({'printed': True})
    #     return self.env.ref('stock.action_report_picking').report_action(self)



  

class CustomerStockmoveFields(models.Model):
  _inherit = "stock.move.line"
  
  cus_package_dat = fields.Char('Pack Qty',  store=True)



  # @api.onchange('quantity_done')
  # def _calculate_package_quantity(self):
  #   if self.quantity_done != '0':
  #     product_box = self.env['product.template'].search([('product_id','=',self.product_id.id)])
  #     print('ghasdfasdascdgascdfa',product_box)



