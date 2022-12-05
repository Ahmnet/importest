odoo.define('import_purchase_order.tree_button', function (require) {
"use strict";
var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');
var ImportPurchaseOrderTreeButton = ListController.extend({
   buttons_template: 'open_import_purchase_order.buttons',
   events: _.extend({}, ListController.prototype.events, {
       'click .open_import_purchase_order_action': '_OpenImportPurchaseOrder',
   }),
   _OpenImportPurchaseOrder: function () {
       var self = this;
        this.do_action({
           type: 'ir.actions.act_window',
           res_model: 'import.purchase.order.wizard',
           name :'Upload File',
           view_mode: 'form',
           view_type: 'form',
           views: [[false, 'form']],
           target: 'new',
           res_id: false,
       });
   }
});
var ImportPurchaseOrderListView = ListView.extend({
   config: _.extend({}, ListView.prototype.config, {
       Controller: ImportPurchaseOrderTreeButton,
   }),
});
viewRegistry.add('import_purchase_order_in_tree', ImportPurchaseOrderListView);
});