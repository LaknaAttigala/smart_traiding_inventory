
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

  cus_product_list=fields.Char("Products List" , compute="_generate_product_list")

  

  @api.multi
  @api.depends("move_lines")
  def _generate_product_list(self):
    for rec in self:
      products =""
      for line in rec.move_lines:   
        if line.product_id.cus_product_id:   
          products = products + "\r\n" + line.product_id.cus_product_id
      rec.cus_product_list = products
  # cus_package_qty = fields.Integer('Pack Qty', store=True)
  

  def do_print_picking(self):
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
      if pick_return[:6] !="Return":
        self.write({'printed': True})
        return self.env.ref('smart_traiding_inventory.menu_action_report_aod_doc').report_action(self)
    else:
      self.write({'printed': True})
      return self.env.ref('stock.action_report_picking').report_action(self)
    # self.write({'printed': True})
    #     return self.env.ref('stock.action_report_picking').report_action(self)



  


class StockMove(models.Model):
  _inherit = "stock.move"
  
  cus_package_count = fields.Integer('Pack Qty',  store=True, )

  @api.onchange('quantity_done')
  def _generate_Package_count(self):
    if self.quantity_done != 0 and self.quantity_done !=0.00:
      pack_count = self.quantity_done/self.product_id.box_quantity
      pack_count = round(pack_count)
      self.cus_package_count=pack_count

class StockMoveLine(models.Model):
  _inherit = "stock.move.line"
  
  cus_package_count = fields.Integer('Pack Qty',  store=True, compute="_generate_Package_count")

  @api.depends('qty_done')
  def _generate_Package_count(self):
    for r in self:
      if r.qty_done != 0 and r.qty_done !=0.00:
        if r.product_id.box_quantity !=0.00:
          pack_count = r.qty_done/r.product_id.box_quantity
          pack_count = round(pack_count)
          r.cus_package_count=pack_count
    # for pack in self:
    #   if pack.product_id.box_quantity != 0.00 and pack.quantity_done !=0.00 :
    #     pack_count = pack.quantity_done / pack.product_id.box_quantity
    #     pack_count = int(pack_count)
    #     pack.cus_package_count=pack_count
  




