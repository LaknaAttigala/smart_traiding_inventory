from flectra import api,fields,models,_
from flectra.exceptions import ValidationError
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('edited','Edited'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),        
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='new')
    #add new State
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'new': [('readonly', False)],'draft': [('readonly', False)], 'edited': [('readonly', False)],'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, states={'new': [('readonly', False)],'draft': [('readonly', False)], 'edited': [('readonly', False)],'sent': [('readonly', False)]}, help="Invoice address for current sales order.")
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'new': [('readonly', False)],'draft': [('readonly', False)], 'edited': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.")
    
    validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False, states={'new': [('readonly', False)],'draft': [('readonly', False)],'edited': [('readonly', False)], 'sent': [('readonly', False)]},
        help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
    cus_order_type= fields.Selection([('sample','Sample Order'),('sales','sale Order')], string='Order Type', default='sales')

    carried_by = fields.Char("Carried By")
    Vehicle_no = fields.Char("Vehicle No")

    #terms and conditions fields
    cus_delivery_terms = fields.Many2one('smart_traiding_inventory.deliverytearm', string='Delivery Terms',  index=True)
    cus_minimum_order = fields.Many2one('smart_traiding_inventory.minimumorder', string='Minimum Order',  index=True)
    cus_tax_condition = fields.Many2one('smart_traiding_inventory.taxcondtions', string='Tax Conditions',  index=True)
    cus_quote_headings = fields.Text(string="Quotation Heading",  index=True)
     
    cus_approved = fields.Many2one('res.users', string="Approved By", store=True, )
    cus_approved_date = fields.Datetime(string="Approved Date")
    ord_type = fields.Selection([
            ('quotation','Quotation'),
            ('order','Order'),
        ], readonly=True, index=True, change_default=True, default=lambda self: self._context.get('ord_type'),
        track_visibility='always')



    # # change create function to default new status
    # @api.model
    # def create(self, vals):              
    #     result = super(SaleOrder, self).create(vals)
    #     # if result.ord_type=="order":
    #     result.write({'state':'new'})       
    #     return result

    #if edit the quotation
    @api.multi
    def write (self, vals):
        if 'state' not in vals.keys() and self.state=="draft" or self.state=="sent":
            vals['state']= 'edited'
        res = super(SaleOrder, self).write(vals)
        print('sssssssssssssssssssssssss   ',vals)
        return res
    # @api.model
    # def write(self, values):
    #     # vals['edit_state']= 'edit'
    #     print('sssssssssssssssssssssssss   ',values)
    #     production = super(SaleOrder, self).write(values)
    #     print('sssssssssssssssssssssssss   ',values)
    #     # if 'state' not in values.keys():
    #     #     production.write({'state':'edited'})
    #     return production

    #approve button action
    @api.multi
    def action_approve(self):
        # self.ensure_one()
        if self.state=="new":
            self.write({'state':'draft','ord_type':'quotation'})
        elif self.state=="edited":
            self.write({'state':'draft','ord_type':'quotation'})


    @api.onchange("ord_type")
    def check_context_test(self):
        if self.ord_type=="order":
            self.state="new"
  
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

    
    @api.multi
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        if res:
            now_date = datetime.now()
            self.cus_approved= self.env.user.id
            self.cus_approved_date= now_date

        return True

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