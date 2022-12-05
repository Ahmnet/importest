from odoo import models, fields
from datetime import datetime

class SyncPurchaseOrderWizard(models.TransientModel):
    _name = 'sync.purchase.order.wizard'
    _description = 'To open popup for user to choose the type to sync the purchase order'

    x_import_purchase_order_ids = fields.Many2many(comodel_name="import.purchase.order", string="Import Purchase Order List")
    x_sync_type = fields.Selection(string="Sync Type", default='sync_draft', selection=[('sync_draft', 'Sync Draft PO'), ('sync_confirmed', 'Sync Confirmed PO'), ], required=False, )

    def sync_purchase_order(self):
        for record in self:
            for import_purchase_order in record.x_import_purchase_order_ids:
                if not import_purchase_order.x_problem:
                    purchase_order = self.env['purchase.order'].search([('name', '=', import_purchase_order.x_po_number)], limit=1)
                    if purchase_order:
                        purchase_order.write({
                            'date_order': import_purchase_order.x_check_confirmation_date or datetime.today(),
                            'date_planned': import_purchase_order.x_check_receipt_date or datetime.today(),
                            'partner_ref': import_purchase_order.x_vendor_reference
                        })
                        self.env['purchase.order.line'].create({
                            'order_id': purchase_order.id,
                            'product_id': import_purchase_order.x_product_id.id,
                            'price_unit': import_purchase_order.x_price,
                            'product_qty': import_purchase_order.x_quantity,
                            'product_uom': import_purchase_order.x_uom_id.id,
                            'taxes_id': [x.id for x in import_purchase_order.x_tax_ids]
                        })
                        if purchase_order.state != 'purchase' and record.x_sync_type == 'sync_confirmed':
                            purchase_order.button_confirm()
                    else:
                        create_purchase_order = self.env['purchase.order'].create({
                            'name': import_purchase_order.x_po_number,
                            'date_order': import_purchase_order.x_check_confirmation_date or datetime.today(),
                            'date_planned': import_purchase_order.x_check_receipt_date or datetime.today(),
                            'partner_id': import_purchase_order.x_vendor_id.id,
                            'partner_ref': import_purchase_order.x_vendor_reference
                        })

                        if create_purchase_order:
                            if record.x_sync_type == 'sync_confirmed':
                                create_purchase_order.button_confirm()
                            self.env['purchase.order.line'].create({
                                'order_id': create_purchase_order.id,
                                'product_id': import_purchase_order.x_product_id.id,
                                'price_unit': import_purchase_order.x_price,
                                'product_qty': import_purchase_order.x_quantity,
                                'product_uom': import_purchase_order.x_uom_id.id,
                                'taxes_id':  [x.id for x in import_purchase_order.x_tax_ids],
                            })
                    import_purchase_order.write({
                        'x_status': 'synced'
                    })