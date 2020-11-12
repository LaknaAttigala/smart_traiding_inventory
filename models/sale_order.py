from flectra import api,fields,models,_
from flectra.exceptions import ValidationError
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    cus_order_type= fields.Selection([('sample','Sample Order'),('sales','sale Order')], string='Order Type', default='sales')

    carried_by = fields.Char("Carried By")
    Vehicle_no = fields.Char("Vehicle No")

    #terms and conditions fields
    cus_delivery_terms = fields.Many2one('smart_traiding_inventory.deliverytearm', string='Delivery Terms',  index=True)
    cus_minimum_order = fields.Many2one('smart_traiding_inventory.minimumorder', string='Minimum Order',  index=True)
    cus_tax_condition = fields.Many2one('smart_traiding_inventory.taxcondtions', string='Tax Conditions',  index=True)
    cus_quote_headings = fields.Text(string="Quotation Heading",  index=True)
     
    cus_approved = fields.Many2one('res.users', string="Approved By", store=True)
    cus_approved_date = fields.Datetime(string="Approved Date")



    # @api.multi
    # def _action_confirm(self):
    #     for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
    #         order.message_subscribe([order.partner_id.id])
    #     now_date = datetime.now()
    #     self.write({
    #         'state': 'sale',
    #         'confirmation_date': fields.Datetime.now(),
    #         'cus_approved':self.env.user.id,
    #         'cus_approved_date':now_date 
    #     })
    #     if self.env.context.get('send_email'):
    #         self.force_quotation_send()

    #     # create an analytic account if at least an expense product
    #     for order in self:
    #         if any([expense_policy not in [False, 'no'] for expense_policy in order.order_line.mapped('product_id.expense_policy')]):
    #             if not order.analytic_account_id:
    #                 order._create_analytic_account()

    #     return True


    # Raise the warning "Minimum order quantity of the product <Name> is <Quantity Value>."
    # if the order quantity is less than the 'Minimum Order Quantity' of the Product.
    @api.constrains('order_line')
    def check_constraint_quantity(self):
        for record in self:
            if record.order_line:
                for product_ids in record.order_line:
                    product = product_ids.product_id.id
                    list_price = self.env['product.product'].browse(product).list_price
                    if product_ids.price_unit < list_price:
                        raise ValidationError(_('Minimum sale price of the product ' +product_ids.name+' is ' +str(list_price)))

    
    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        if self.cus_order_type=="sample":
            return self.env.ref('smart_traiding_inventory.menu_action_report_sampleorder').report_action(self)
        else:
            return self.env.ref('sale.action_report_saleorder').report_action(self)

    
    # @api.multi
    # def _action_confirm(self):
    #     for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
    #         order.message_subscribe([order.partner_id.id])
    #     self.write({
    #         'state': 'sale',
    #         'confirmation_date': fields.Datetime.now()
    #     })
    #     if self.env.context.get('send_email'):
    #         self.force_quotation_send()

    #     # create an analytic account if at least an expense product
    #     for order in self:
    #         if any([expense_policy not in [False, 'no'] for expense_policy in order.order_line.mapped('product_id.expense_policy')]):
    #             if not order.analytic_account_id:
    #                 order._create_analytic_account()

    #     return True


    @api.onchange('state')
    def get_approved_user(self):   
          
        now_date = datetime.now()
        self.cus_approved= self.env.user.id
        self.cus_approved_date= now_date
        print("hdssssssskkkkkhassssssssssssssss777777777777777777 ", self.state, self.cus_approved, self.cus_approved_date)
        
      
        # self.write({
        #     'cus_approved':self.env.user.id,
        #     'cus_approved_date':now_date 
        # })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
   

    cus_is_return = fields.Boolean('Rerurn')




class CusDeliveryTerms(models.Model):
    _name = 'smart_traiding_inventory.deliverytearm'
   

    name = fields.Char('Detail')




class MinimumOrderTerms(models.Model):
    _name = 'smart_traiding_inventory.minimumorder'
   

    name = fields.Char('Detail')


class TaxConditionsTerms(models.Model):
    _name = 'smart_traiding_inventory.taxcondtions'
   

    name = fields.Char('Detail')