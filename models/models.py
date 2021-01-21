# -*- coding: utf-8 -*-
from datetime import datetime
from flectra import models, fields, api,_

# class smart_traiding_inventory(models.Model):
#     _name = 'smart_traiding_inventory.smart_traiding_inventory'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    age = fields.Integer(string="Age",  compute="_compute_age")
    blood_group= fields.Char(string="Blood Group")

    @api.multi
    @api.depends("birthday")
    def _compute_age(self):
      for record in self:
        today = datetime.now().year
        age=0
        if record.birthday:
          birth = datetime.strptime(record.birthday, "%Y-%m-%d").year
          age= today - birth
        # age = 0
        # if record.birthday:
        #   age = relativedelta(
        #     fields.Date.today(),
        #     record.birthday,
        #   ).years
        record.age = age

class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"
 
    description = fields.Char('Description')

# class StockQuantityHistory(models.TransientModel):
#     _inherit = 'stock.quantity.history'
 
#     def export_xls(self):
#       self.ensure_one()
#       context = self._context
#       datas = {'ids': context.get('active_ids', [])}
#       datas['model'] = 'stock.quantity.history'
#       datas['form'] = self.read()[0]
#       # for field in datas['form'].keys():
#       #   if isinstance(datas['form'][field], tuple):
#       #     datas['form'][field] = datas['form'][field][0]
#       if context.get('xls_export'):
#         return self.env.ref('smart_traiding_inventory.export_stock_valuation_excel').report_action(self, data=datas)

class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    compute_at_date = fields.Selection([
      (0, 'Current Inventory'),
      (1, 'At a Specific Date')
    ], string="Compute", help="Choose to analyze the current inventory or from a specific date in the past.", default=1)

    def open_table(self):
      self.ensure_one()
      if self.env.context.get('valuation'):
        if self.compute_at_date:
          tree_view_id = self.env.ref('stock_account.view_stock_product_tree2').id
          form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
          action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'view_mode': 'tree,form',
            'name': _('Products'),
            'res_model': 'product.product',
            'domain': "[('type', '=', 'product'), ('qty_available', '!=', 0)]",
            'context': dict(self.env.context, to_date=self.date, company_owned=True),
          }
          return action
        else:
          return self.env.ref('stock_account.product_valuation_action').read()[0]
      else:
        tree_view_id = self.env.ref('stock.view_stock_product_tree').id
        form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
        action = {
          'type': 'ir.actions.act_window',
          'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
          'view_mode': 'tree,form',
          'name': _('Products'),
          'res_model': 'product.product',
          'context': dict(self.env.context, to_date=self.date),
        }
        return action

        # if self.compute_at_date:
      