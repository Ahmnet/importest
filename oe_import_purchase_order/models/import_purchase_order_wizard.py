from odoo import models, fields, api
import tempfile
import binascii
import logging
import base64
import io
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

try:
    import xlrd
except ImportError:
    print("Cannot import xlrd")
    _logger.debug('Cannot `import xlrd`.')

class ImportPurchaseOrderWizard(models.TransientModel):
    _name = 'import.purchase.order.wizard'
    _description = 'To open wizard for user to upload file'

    x_file_binary = fields.Binary(string="Binary")
    x_filename = fields.Char(string="File Name", required=False, )

    def get_po_excel_template(self):
        url = str('/oe_import_purchase_order/static/src/xls/purchaseordertemplate.xlsx')
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'self', 'tag': 'reload', }

    def get_po_csv_template(self):
        url = str('/oe_import_purchase_order/static/src/xls/purchaseordertemplate.csv')
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'self', 'tag': 'reload', }

    def import_purchase_order(self):
        try:
            if self.x_filename.strip().endswith('.csv') or self.x_filename.strip().endswith('.xlsx'):
                if self.x_filename.strip().endswith('.xlsx'):
                    fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                    fp.write(binascii.a2b_base64(self.x_file_binary))
                    fp.seek(0)
                    book = xlrd.open_workbook(fp.name)
                    for sheet in book.sheets():
                        try:
                            if sheet.name == 'Sheet1':
                                for row in range(sheet.nrows):
                                    if row >= 1:
                                        row_values = sheet.row_values(row)
                                        self._create_import_purchase_order(row_values)
                            return {
                                'type': 'ir.actions.client',
                                'tag': 'reload',
                            }
                        except IndexError:
                            raise UserError("Please make sure that you did not change our template. Make sure all excel column are there, and to begin with name Sheet1. Download our sample first!")
                else:
                    keys = ['PO Number', 'Vendor Name', 'Vendor Reference', 'Confirmation Date', 'Receipt Date', 'Product', 'Quantity', 'UOM', 'Price', 'Tax']
                    try:
                        csv_data = base64.b64decode(self.x_file_binary)
                        data_file = io.StringIO(csv_data.decode("utf-8"))
                        data_file.seek(0)
                        file_reader = []
                        csv_reader = csv.reader(data_file, delimiter=',')
                        file_reader.extend(csv_reader)
                    except:
                        raise UserError("Invalid file!")
                    for i in range(len(file_reader)):
                        field = list(map(str, file_reader[i]))
                        values = dict(zip(keys, field))
                        if values:
                            if i == 0:
                                continue
                            else:
                                self._create_import_purchase_order(field)
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                    }
            else:
                raise UserError("The uploaded file should be csv or excel format")

        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.x_filename)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')


    def _create_import_purchase_order(self, import_purchase_order_values):
        if len(import_purchase_order_values) >= 10:
            self.env['import.purchase.order'].create({
                'x_po_number': False if import_purchase_order_values[0] == '' else import_purchase_order_values[0],
                'x_vendor_name': False if import_purchase_order_values[1] == '' else import_purchase_order_values[1],
                'x_vendor_reference': False if import_purchase_order_values[2] == '' else import_purchase_order_values[2],
                'x_confirmation_date':False if import_purchase_order_values[3] == '' else import_purchase_order_values[3],
                'x_receipt_date':False if import_purchase_order_values[4] == '' else import_purchase_order_values[4],
                'x_product_name': False if import_purchase_order_values[5] == '' else import_purchase_order_values[5],
                'x_quantity': False if import_purchase_order_values[6] == '' else import_purchase_order_values[6],
                'x_uom': False if import_purchase_order_values[7] == '' else import_purchase_order_values[7],
                'x_price': False if import_purchase_order_values[8] == '' else import_purchase_order_values[8],
                'x_tax': False if import_purchase_order_values[9] == '' else import_purchase_order_values[9],
            })
        else:
            raise UserError("There should be 10 column in your file")