
# -*- coding:utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
from flectra import api, fields, models, SUPERUSER_ID, _
from flectra.exceptions import UserError, AccessError, ValidationError
from flectra.tools.float_utils import float_compare
from flectra.addons import decimal_precision as dp
from datetime import datetime



class AccountInvoice(models.Model):
  
  _inherit = 'account.invoice'

  cus_approved = fields.Many2one('res.users', string="Approved By", readonly=True, store=True)
  cus_approved_date = fields.Datetime(string="Approved Date", readonly=True)

  cusdec_no = fields.Char('Cusdec No')
  reference = fields.Char(string='Invoice Number')
  cus_source = fields.Char('Reference')
  grn_numbers = fields.Char('GRN Numbers')

  stock_picking_ids = fields.Many2many(
    comodel_name='stock.picking',
    string= 'Grn No List',
    domain=([('cus_paid','=','None'), ('picking_type_code','=','incoming')]),
  )



  @api.multi
  def action_invoice_paid(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
    to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
    if to_pay_invoices.filtered(lambda inv: inv.state != 'open'):
      raise UserError(_('Invoice must be validated in order to set it to register payment.'))
    if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
      raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
    
    if self.number:
      purchase_line = self.env['account.invoice.line'].search([('invoice_id','=',self.id)])
      for rec in purchase_line:
        picking_id = self.env['stock.picking'].search([('name','=',rec.grn_id)])
        picking_id.write({'cus_paid':'paid'})
     
    return to_pay_invoices.write({'state': 'paid'})


  @api.multi
  def invoice_validate(self):
    for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
      invoice.message_subscribe([invoice.partner_id.id])
    self._check_duplicate_supplier_reference()
    now_date = datetime.now()
    return self.write({'state': 'open','cus_approved':self.env.user.id,'cus_approved_date':now_date })


  @api.model
  def create(self, vals):
    invoice = super(AccountInvoice, self).create(vals)
    # purchase = invoice.invoice_line_ids.mapped('purchase_line_id.order_id')
    # if purchase and not invoice.refund_invoice_id:
    #   message = _("This vendor bill has been created from: %s") % (",".join(["<a href=# data-oe-model=purchase.order data-oe-id="+str(order.id)+">"+order.name+"</a>" for order in purchase]))
    #   invoice.message_post(body=message)
    return invoice

  # @api.onchange('invoice_line_ids')
  # def _onchange_origin(self):
  #   res= super(AccountInvoice, self)._onchange_origin(self)
  #   grn_ids = self.invoice_line_ids.mapped('stock_picking_ids')
  #   if grn_ids:
  #     self.grn_numbers = ', '.join(grn_ids.mapped('name'))
  #   # purchase_ids = self.invoice_line_ids.mapped('purchase_id')
  #   # if purchase_ids:
  #   #   self.origin = ', '.join(purchase_ids.mapped('name'))
  #   return res


  @api.multi
  @api.onchange('purchase_id','partner_id')
  def _select_stovk_numbers(self):
    result = {}
    if self.purchase_id:      # purchases_id = self.env['purchase.order'].search([('name','=',self.purchase_id.name)])

      domain = [('cus_paid','=','None'), ('picking_type_code','=','incoming'),('purchase_id','=',self.purchase_id.id),('partner_id','=',self.partner_id.id)]
      result['domain'] = {'stock_picking_ids':domain}    
    
    return result


  def _prepare_invoice_line_from_po_line(self, line,stock_noss,purchase_id):
     
    tax_detail = self.env['purchase.order.line'].search([('product_id','=',purchase_id.id)])
    if tax_detail:
      for s in tax_detail:
        taxes = s.taxes_id
    else:
      taxes =""
    invoice_line_tax_ids = purchase_id.fiscal_position_id.map_tax(taxes)
    invoice_line = self.env['account.invoice.line']
    purchase_order = self.env['purchase.order.line'].search([('product_id','=',line.product_id.id),('order_id','=',self.purchase_id.id)])
    price_unit =self.env['purchase.order.line'].search([('product_id','=',line.product_id.id),('order_id','=',self.purchase_id.id)]).price_unit, self.env['purchase.order.line'].search([('product_id','=',line.product_id.id),('order_id','=',self.purchase_id.id)]).price_unit
       

    if float_compare(line.qty_done, 0.0, precision_rounding=line.move_id.product_uom.rounding) <= 0:
      line.qty_done = 0.0
    data = {
      'purchase_line_id': purchase_order.id,
      'name': purchase_id.name+': '+line.product_id.name,
      'origin': purchase_id.origin,
      'grn_id': line.picking_id.name,
      'uom_id': line.product_uom_id,
      'product_id': line.product_id.id,
      'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
      # 'price_unit':purchase_order.price_unit,
      'price_unit': purchase_id.currency_id.with_context(date=self.date_invoice).compute(purchase_order.price_unit,self.currency_id, round=False),
            # 'price_unit': purchase_id.currency_id.with_context(date=self.date_invoice).compute(purchase_id.order_line.with_context(prduct_id=line.product_id.id).price_unit, purchase_id.order_line.with_context(prduct_id=line.product_id.id).currency_id, round=False),
      'quantity': line.qty_done,
      'discount': 0.0,
      'account_analytic_id': purchase_order.account_analytic_id.id,
      'analytic_tag_ids': purchase_order.analytic_tag_ids.ids,
      'invoice_line_tax_ids': invoice_line_tax_ids.ids
    }
       
    account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, purchase_id.fiscal_position_id, self.env.user.company_id)
    if account:
      data['account_id'] = account.id
    return data


  @api.onchange('stock_picking_ids')
  def purchase_order_change(self):
    if not self.stock_picking_ids:
      return {}
    if not self.partner_id:
      self.partner_id = self.stock_picking_ids.partner_id.id

    vendor_ref = self.purchase_id.partner_ref
    if vendor_ref:
      self.reference = ", ".join([self.reference, vendor_ref]) if (
        self.reference and vendor_ref not in self.reference) else vendor_ref

    new_lines = self.env['account.invoice.line']
    purchase_id = self.purchase_id
    stock_noss = self.stock_picking_ids
    
    for line in self.stock_picking_ids.move_line_ids:
      # print('gsdgfdshfshfgvhdvff',self.invoice_line_ids)
      # print('6465465464664564',line.product_id)
      data = self._prepare_invoice_line_from_po_line(line, stock_noss,purchase_id)
      new_line = new_lines.new(data)
      new_line._set_additional_fields(self)
      new_lines += new_line
    if self.grn_numbers:
      self.grn_numbers = self.grn_numbers+","+ self.stock_picking_ids.name
    else:
      self.grn_numbers = self.stock_picking_ids.name
    self.invoice_line_ids += new_lines
    self.payment_term_id = self.purchase_id.payment_term_id
    self.env.context = dict(self.env.context, from_purchase_order_change=True)
    # self.purchase_id = True
    self.stock_picking_ids = False
    return {}





  

class AccountInvoiceLine(models.Model):
  
  _inherit = 'account.invoice.line'


  quantity = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        required=True, default=1)
  stock_pick_id = fields.Many2one('purchase.order' ,related='purchase_id', string='Stock ID', store=False, readonly=True,)
  stock_detail = fields.Many2many('stock.picking', related='stock_pick_id.picking_ids', string='stock', copy=True, store=False)
  grn_id = fields.Char (string='GRN No(s)', store=True, )
  # #grn_id = fields.Char(string='GRN IDS')

  @api.multi
  @api.depends('stock_detail','stock_pick_id','purchase_id')  
  def _setgrnids(self):
    # if self.stock_pick_id:
    #   stocks = self.env['stock.picking'].search([('origin','=',self.stock_pick_id.name)])
    #   print("@#@#@#@@@@@@@@@@@@@@@@@@@@@@   ", stocks)

    # print("hgavdhutafsgsfchgdscfdghfscgdacsf",self.purchase_id.name )
    for rec in self:
      grn_ids=''
      if rec.stock_detail:
        for val in rec.stock_detail:
          grn_ids = grn_ids+ '\n'+ val.name
    
      rec.grn_id = grn_ids
    