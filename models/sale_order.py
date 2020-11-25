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