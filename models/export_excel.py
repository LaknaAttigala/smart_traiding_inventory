
from datetime import date, timedelta, datetime
from flectra.exceptions import UserError
from flectra import api, models, _


class resPartnerDetailsXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.res_partner_excel_reportss'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 12 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Master Data')



    sheet.merge_range('F2:L3','Master Data',top_header) #Total Allowance 
        # sheet.right_to_left()
        
    # sheet.set_column(3, 3, 50)
    # sheet.set_column(2, 2, 30)
    # sheet.write('C5', 'EPF', tabel_header)
    sheet.merge_range('B5:C6','Name',tabel_header) #Total Allowance 
    sheet.merge_range('D5:G6','Address',tabel_header) #Total Allowance 
    sheet.merge_range('H5:I6','Contact Number',tabel_header) #Total Allowance 
    sheet.merge_range('J5:K6','Email',tabel_header) #Total Allowance 
    sheet.merge_range('L5:M6','TIN',tabel_header) #Total Allowance 
    sheet.merge_range('N5:O6','VAT',tabel_header) #Total Allowance
    sheet.merge_range('P5:Q6','SVAT',tabel_header) #Total Allowance
    sheet.merge_range('R5:S6','BR Number',tabel_header) #Total Allowance
    sheet.merge_range('T5:V6','TAGS',tabel_header) #Total Allowance
    sheet.merge_range('W5:Z6','Payment Terms',tabel_header) #Total Allowance 
    sheet.merge_range('AA5:AC6','Customer/Supplier',tabel_header) #Total Allowance 
    sheet.merge_range('AD5:AG6','Comments',tabel_header) #Total Allowance 

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.name,format2)
        address=""
        if pick.street:
            address = address + pick.street
        if pick.street2:
            address = address + "," + pick.street2
        if pick.city:
            address = address + "," +  pick.city 
        if pick.state_id:
            address = address + "," +  pick.state_id.name
        if pick.zip :
            address = address + "," +  pick.zip
        if pick.country_id:
            address = address + "," +  pick.country_id.name

        sheet.merge_range('D%d:G%d'  %(data_row,data_row),address,format2)
        contact=""
        if pick.phone:
            contact = contact + pick.phone
        if pick.mobile:
            contact = contact + pick.mobile
        sheet.merge_range('H%d:I%d'  %(data_row,data_row),contact,format2)
        
        sheet.merge_range('J%d:K%d'  %(data_row,data_row),pick.email,format2)
        sheet.merge_range('L%d:M%d'  %(data_row,data_row),pick.vat,format2)
        sheet.merge_range('N%d:O%d'  %(data_row,data_row),pick.vat2,format2)
        sheet.merge_range('P%d:Q%d'  %(data_row,data_row),pick.svat,format2)
        sheet.merge_range('R%d:S%d'  %(data_row,data_row),pick.br_number,format2)
        tags =""
        for cat in pick.category_id:
            tags = tags +" "+ cat.name
        sheet.merge_range('T%d:V%d'  %(data_row,data_row),tags,format2)
        payemt=""
        if pick.supplier and pick.property_supplier_payment_term_id.name :
            payemt ="Supplier :- "+pick.property_supplier_payment_term_id.name
        if pick.customer and pick.property_payment_term_id.name:
            payemt = payemt + " / " +"customer :- "+pick.property_payment_term_id.name
        sheet.merge_range('W%d:Z%d'  %(data_row,data_row),payemt,format2)
        customer=""
        if pick.supplier:
            customer =customer+"Supplier "
        if pick.customer:
            customer =customer+" Customer"
        sheet.merge_range('AA%d:AC%d'  %(data_row,data_row),customer,format2)
        sheet.merge_range('AD%d:AG%d'  %(data_row,data_row),pick.comment,format2)

            
        data_row +=1
        


class productTemplateXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.product_template_excel_reportss'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 12 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Master Data')



    sheet.merge_range('F2:L3','Master Data',top_header) #Total Allowance 
        # sheet.right_to_left()
        
    # sheet.set_column(3, 3, 50)
    # sheet.set_column(2, 2, 30)
    # sheet.write('C5', 'EPF', tabel_header)
    sheet.merge_range('B5:C6','Product ID',tabel_header) #Total Allowance 
    sheet.merge_range('D5:F6','Product Name',tabel_header) #Total Allowance 
    sheet.merge_range('G5:H6','Product Type',tabel_header) #Total Allowance 
    sheet.merge_range('I5:J6','Category',tabel_header) #Total Allowance 
    sheet.merge_range('K5:L6','Minimum \n sales price',tabel_header) #Total Allowance 
    sheet.merge_range('M5:N6','Cost',tabel_header) #Total Allowance
    sheet.merge_range('O5:P6','Quantity Per Box',tabel_header) #Total Allowance
    sheet.merge_range('Q5:R6','Quantity \n on Hand',tabel_header) #Total Allowance
    sheet.merge_range('S5:T6','Weight',tabel_header) #Total Allowance
    sheet.merge_range('U5:V6','Volume',tabel_header) #Total Allowance 
    sheet.merge_range('W5:X6','Length',tabel_header) #Total Allowance 
    sheet.merge_range('Y5:Z6','Width',tabel_header) #Total Allowance 
    sheet.merge_range('AA5:AC6','Responsible',tabel_header) #Total Allowance 
    sheet.merge_range('AD5:AF6','Description for internal',tabel_header) #Total Allowance 

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.cus_product_id,format2)
        sheet.merge_range('D%d:F%d'  %(data_row,data_row),pick.name,format2)
        sheet.merge_range('G%d:H%d'  %(data_row,data_row),pick.type,format2)
        sheet.merge_range('I%d:J%d'  %(data_row,data_row),pick.categ_id.name,format2)
        sheet.merge_range('K%d:L%d'  %(data_row,data_row),pick.list_price,format2)
        sheet.merge_range('M%d:N%d'  %(data_row,data_row),pick.standard_price,format2)
        sheet.merge_range('O%d:P%d'  %(data_row,data_row),pick.box_quantity,format2)
        sheet.merge_range('Q%d:R%d'  %(data_row,data_row),pick.qty_available,format2)
        sheet.merge_range('S%d:T%d'  %(data_row,data_row),pick.weight,format2)
        sheet.merge_range('U%d:V%d'  %(data_row,data_row),pick.volume,format2)
        sheet.merge_range('W%d:X%d'  %(data_row,data_row),pick.cus_length,format2)
        sheet.merge_range('Y%d:Z%d'  %(data_row,data_row),pick.cus_width,format2)
        sheet.merge_range('AA%d:AC%d'  %(data_row,data_row),pick.responsible_id.name,format2)
        if pick.description:
            sheet.merge_range('AD%d:AF%d'  %(data_row,data_row),pick.description,format2)
        else:
            sheet.merge_range('AD%d:AF%d'  %(data_row,data_row),"",format2)
    
        data_row +=1

class productVarientsTemplateXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.product_varients_excel_reportss'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 12 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Master Data')



    sheet.merge_range('F2:L3','Master Data',top_header) #Total Allowance 
        # sheet.right_to_left()
        
    # sheet.set_column(3, 3, 50)
    # sheet.set_column(2, 2, 30)
    # sheet.write('C5', 'EPF', tabel_header)
    sheet.merge_range('B5:C6','Product ID',tabel_header) #Total Allowance 
    sheet.merge_range('D5:F6','Product Name',tabel_header) #Total Allowance 
    sheet.merge_range('G5:I6','Attributes',tabel_header) #Total Allowance 
    sheet.merge_range('J5:K6','Sale Price',tabel_header) #Total Allowance 
    sheet.merge_range('L5:M6','Quantity \n on Hand',tabel_header) #Total Allowance
    sheet.merge_range('N5:O6','Forcast \n Quantity',tabel_header) #Total Allowance
    sheet.merge_range('P5:Q6','Barcode',tabel_header) 

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.cus_product_id,format2)
        sheet.merge_range('D%d:F%d'  %(data_row,data_row),pick.name,format2)
        attr =""
        if pick.attribute_value_ids:
            for n in pick.attribute_value_ids:
                attr = attr +" "+ n.attribute_id.name+":"+n.name
        sheet.merge_range('G%d:I%d'  %(data_row,data_row),attr,format2)

        sheet.merge_range('J%d:K%d'  %(data_row,data_row),pick.lst_price,format2)
        sheet.merge_range('L%d:M%d'  %(data_row,data_row),pick.qty_available,format2)
        sheet.merge_range('N%d:O%d'  %(data_row,data_row),pick.virtual_available,format2)
        sheet.merge_range('P%d:Q%d'  %(data_row,data_row),pick.barcode,format2)
        
        data_row +=1
        
        
    
class productPackageTemplateXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.product_packages_excel_reportss'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 12 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Master Data')



    sheet.merge_range('D2:L3','Package',top_header) #Total Allowance 
        # sheet.right_to_left()
        
    # sheet.set_column(3, 3, 50)
    # sheet.set_column(2, 2, 30)
    # sheet.write('C5', 'EPF', tabel_header)
    sheet.merge_range('B5:C6','Package Name',tabel_header) #Total Allowance 
    sheet.merge_range('D5:E6','Product ID',tabel_header) #Total Allowance 
    sheet.merge_range('F5:G6','Product Name',tabel_header) #Total Allowance 
    sheet.merge_range('H5:I6','Quantity',tabel_header) #Total Allowance 

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.name,format2)
        sheet.merge_range('D%d:E%d'  %(data_row,data_row),pick.product_id.cus_product_id,format2)
        sheet.merge_range('F%d:G%d'  %(data_row,data_row),pick.product_id.name,format2)
        sheet.merge_range('H%d:I%d'  %(data_row,data_row),pick.qty,format2)
        
        data_row +=1
        
        
class stockValuationsDetailsXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.export_stock_valuation_excelv'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
  
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 11 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Inventory')
   
    
  
    sheet.merge_range('D2:L3','Inventory',top_header) #Total Allowance 
        # sheet.right_to_left()

    sheet.merge_range('B5:C6','Product ID',tabel_header) #Total Allowance 
    sheet.merge_range('D5:E6','Product Name',tabel_header) #Total Allowance 
    sheet.merge_range('F5:G6','Qunatity \n on Hand',tabel_header) #Total Allowance 
    sheet.merge_range('H5:I6','Forecast \n Quantity',tabel_header) #Total Allowance 

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.cus_product_id,format2)
        sheet.merge_range('D%d:E%d'  %(data_row,data_row),pick.name,format2)
        sheet.merge_range('F%d:G%d'  %(data_row,data_row),pick.qty_available,format2)
        sheet.merge_range('H%d:I%d'  %(data_row,data_row),pick.virtual_available,format2)
        
        data_row +=1

      
class stockValuaDetailsXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.export_stock_valu_excelv'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
  
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 10 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Inventory')
   
    
  
    sheet.merge_range('D2:L3','Inventory',top_header) #Total Allowance 
        # sheet.right_to_left()

    sheet.merge_range('B5:C6','Product ID',tabel_header) #Total Allowance 
    sheet.merge_range('D5:E6','Product Name',tabel_header) #Total Allowance 
    sheet.merge_range('F5:G6','Quantity',tabel_header) #Total Allowance 
    sheet.merge_range('H5:I6','Unit of Measures',tabel_header) #Total Allowance 
    sheet.merge_range('J5:K6','Unit Price',tabel_header) #Total Allowance 
    sheet.merge_range('L5:M6','Value',tabel_header) #Total Allowance 

  

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.cus_product_id,format2)
        sheet.merge_range('D%d:E%d'  %(data_row,data_row),pick.name,format2)
        sheet.merge_range('F%d:G%d'  %(data_row,data_row),pick.qty_at_date,format2)
        sheet.merge_range('H%d:I%d'  %(data_row,data_row),pick.uom_id.name,format2)
        sheet.merge_range('J%d:K%d'  %(data_row,data_row),pick.lst_price,format2)
        
        sheet.merge_range('L%d:M%d'  %(data_row,data_row),pick.stock_value,format2)
        
        data_row +=1

class stockOpersDetailsXLS(models.AbstractModel):
  _name = 'report.smart_traiding_inventory.export_stock_oper_excelv'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, lines):
  
    top_header = workbook.add_format({'font_size': 12, 'align': 'center', 'bg_color':'#1ad9d6' ,'bold': True, 'border':2})
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter','border' : 1 })
    tabel_header = workbook.add_format({'font_size': 10 ,'bg_color':'#1ad9d6' ,'align': 'vcenter', 'bold': True,'border':1})
    sheet = workbook.add_worksheet('Inventory')
   
    
  
    sheet.merge_range('D2:L3','Stock Operations',top_header) #Total Allowance 
        # sheet.right_to_left()

    sheet.merge_range('B5:C6','Reference',tabel_header) #Total Allowance 
    sheet.merge_range('D5:E6','Destination Loaction',tabel_header) #Total Allowance 
    sheet.merge_range('F5:G6','Vendor',tabel_header) #Total Allowance 
    sheet.merge_range('H5:I6','Schedule Date',tabel_header) #Total Allowance 
    sheet.merge_range('J5:K6','PO Number',tabel_header) #Total Allowance 
    sheet.merge_range('L5:M6','Product List',tabel_header) #Total Allowance 
    sheet.merge_range('N5:O6','Created By',tabel_header) #Total Allowance 
    sheet.merge_range('P5:Q6','Status',tabel_header) #Total Allowance 

  

    data_row = 7
    row_no =1
    for pick in lines:
        sheet.merge_range('B%d:C%d'  %(data_row,data_row),pick.name,format2)
        sheet.merge_range('D%d:E%d'  %(data_row,data_row),pick.location_dest_id.name,format2)
        sheet.merge_range('F%d:G%d'  %(data_row,data_row),pick.partner_id.name,format2)
        sheet.merge_range('H%d:I%d'  %(data_row,data_row),pick.scheduled_date,format2)
        sheet.merge_range('J%d:K%d'  %(data_row,data_row),pick.origin,format2)
        prod=""
        if pick.move_lines:
                for pro in pick.move_lines:
                    if prod =="":
                        prod = pro.product_id.name
                    else:
                        prod = prod +" , "+pro.product_id.name
        sheet.merge_range('L%d:M%d'  %(data_row,data_row),prod,format2)
        sheet.merge_range('N%d:O%d'  %(data_row,data_row),pick.create_uid.name,format2)
        sheet.merge_range('P%d:Q%d'  %(data_row,data_row),pick.state,format2)
        
        data_row +=1