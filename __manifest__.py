# -*- coding: utf-8 -*-
{
    'name': "smart traiding inventory",

    'summary': """
        Smart trading inventory""",

    'description': """
       Smart trading
    """,

    'author': "DM Prabath",
    'website': "http://codeso.lk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase','purchase_requisition','stock','sale_stock','sale','report_xlsx','stock_landed_costs','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/change_menu.xml',
        'views/invoice_form.xml',
        'views/vender_view_form.xml',        
        'views/stock_picking.xml',
        'views/sale_order.xml',
        'wizard/purchase_order_cancel_button_wizard.xml',
        'views/purchase_order_cancel_button.xml',
        'views/company_new_field.xml',
        'views/vender_bill.xml',
        'views/product_view.xml',
        'views/views.xml',
        
        
        'report/report_header_layout_internal.xml',
        'report/sample_sales_order_report.xml',
        'report/purchase_request_report.xml',
        'report/new_report_menu_purchase.xml',  
        'report/stock_picking_grn_normal.xml',  
        # # 'report/payslip_report_new.xml',    

        'report/report_header_boxed.xml',
        'report/purchase_report.xml',
        'report/purchase_quotation_new_report.xml',
        'report/sales_quotation_order_report.xml',
        # 'report/sale_picking_aod_details.xml',
        'report/sale_picking_aod_doc.xml',
        'report/invoices_bill_report.xml',
        'report/purchase_agreement.xml',
        'report/landed_cost_document.xml',
        'report/inventory_report.xml',


    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'application':True,
}