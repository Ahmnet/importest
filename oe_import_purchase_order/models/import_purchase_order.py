from odoo import models, fields, api
from datetime import datetime


class ImportPurchaseOrder(models.Model):
    _name = 'import.purchase.order'
    _description = 'This model is used to store the value of purchase order from importing excel and csv'

    x_po_number = fields.Char(string="PO Number", required=False, )
    x_vendor_name = fields.Char(string="Vendor", required=False, )
    x_vendor_reference = fields.Char(string="Vendor Reference", required=False, )
    x_confirmation_date = fields.Char(string="Confirmation Date", required=False, )
    x_receipt_date = fields.Char(string="Receipt Date", required=False, )
    x_product_name = fields.Char(string="Product", required=False, )
    x_quantity = fields.Char(string="Quantity", required=False, )
    x_uom = fields.Char(string="UOM", required=False, )
    x_price = fields.Char(string="Price", required=False, )
    x_tax = fields.Char(string="Tax", required=False)

    x_vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor Id", required=False,
                                  compute="_compute_vendor_id")
    x_product_id = fields.Many2one(comodel_name="product.product", string="Product Id", required=False,
                                   compute="_compute_product_id")
    x_uom_id = fields.Many2one(comodel_name="uom.uom", string="UOM Id", required=False, compute="_compute_uom_id")
    x_tax_ids = fields.Many2many(comodel_name="account.tax", string="Tax", compute="_compute_tax_ids")
    x_tax_problem = fields.Char(string="Tax Problem", required=False, )
    x_check_confirmation_date = fields.Char(string="Check Format Date", required=False,
                                            compute="_compute_check_confirmation_date")
    x_check_receipt_date = fields.Char(string="Check Receipt Date", required=False,
                                       compute="_compute_check_receipt_date")
    x_problem = fields.Text(string="Problem", required=False, compute="_compute_problem" )
    x_status = fields.Selection(string="Status", default='not_sync',
                                selection=[('not_sync', 'Not Sync'), ('synced', 'Synced'), ], required=False, )

    @api.depends('x_vendor_name')
    def _compute_vendor_id(self):
        for record in self:
            record['x_vendor_id'] = self.env['res.partner'].search([('name', '=ilike', record.x_vendor_name)], limit=1)

    @api.depends('x_product_name')
    def _compute_product_id(self):
        for record in self:
            record['x_product_id'] = self.env['product.product'].search([('name', '=ilike', record.x_product_name)],
                                                                        limit=1)

    @api.depends('x_uom')
    def _compute_uom_id(self):
        for record in self:
            record['x_uom_id'] = self.env['uom.uom'].search([('name', '=ilike', record.x_uom)], limit=1)

    @api.depends('x_tax')
    def _compute_tax_ids(self):
        for record in self:
            tax_problem = ""
            tax = []
            if record.x_tax:
                for tax_name in record.x_tax.split(','):
                    search_tax = self.env['account.tax'].search([('name', '=ilike', tax_name.strip())], limit=1)
                    if not search_tax:
                        tax_problem = tax_problem + "Tax Name: " + str(tax_name) + " not found, <br/>"
                    else:
                        tax.append(search_tax.id)
            record['x_tax_ids'] = tax
            record['x_tax_problem'] = tax_problem

    def _get_date_format(self):
        date_format = ""
        global_format = self.env['res.lang'].search([('active', '=', True)], limit=1)
        if global_format:
            date_format = global_format.date_format
        return date_format

    @api.depends('x_confirmation_date')
    def _compute_check_confirmation_date(self):
        for record in self:
            date_format = False
            try:
                if record.x_confirmation_date:
                    date_format = datetime.strptime(record.x_confirmation_date, self._get_date_format())
            except ValueError:
                date_format = False
            record['x_check_confirmation_date'] = date_format

    @api.depends('x_receipt_date')
    def _compute_check_receipt_date(self):
        for record in self:
            date_format = False
            try:
                if record.x_receipt_date:
                    date_format = datetime.strptime(record.x_receipt_date, self._get_date_format())
            except ValueError:
                date_format = False
            record['x_check_receipt_date'] = date_format

    @api.depends('x_po_number','x_vendor_id', 'x_product_id', 'x_uom_id', 'x_tax_problem', 'x_check_confirmation_date', 'x_check_receipt_date')
    def _compute_problem(self):
        for record in self:
            problem = ""
            if not record.x_po_number:
                problem = problem + "The PO Number is required <br/>"
            if not record.x_quantity:
                problem = problem + "The quantity of product is required <br/>"
            if not record.x_vendor_id:
                problem = problem + "The vendor name " + str(record.x_vendor_name) + " not found, <br/>"
            if not record.x_product_id:
                problem = problem + "The product name " + str(record.x_product_name) + " not found, <br/>"
            if not record.x_uom_id:
                problem = problem + "The UOM name " + str(record.x_uom) + " not found, <br/>"
            if record.x_tax_problem:
                problem = problem + str(record.x_tax_problem)
            if not record.x_check_confirmation_date and record.x_confirmation_date:
                problem = problem + "The formate date of " + str(record.x_confirmation_date) + " not found, <br/>"
            if not record.x_check_receipt_date and record.x_receipt_date:
                problem = problem + "The formate date of " + str(record.x_receipt_date) + " not found, <br/>"
            record['x_problem'] = problem

    def sync_purchase_order(self):
        return {
            'name': "Sync Type",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('oe_import_purchase_order.view_sync_purchase_order_form_wizard').id,
            'res_model': 'sync.purchase.order.wizard',
            'target': 'new',
            'context': {
                'default_x_import_purchase_order_ids': [import_purchase_order_id.id for import_purchase_order_id in self],
            }

        }


