{
    'name': 'Import Purchase Order',
    'version': '15.0.0.1.0.0',
    'summary': 'Import purchase order and purchase order line follow the template',
    'description': 'Import purchase order and purchase order line follow the template',
    'category': 'Purchase',
    'price': "5.68",
    'currency': "USD",
    'author': 'OE Dev',
    'website': 'https://oe-dev.odoo.com/',
    'license': 'OPL-1',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/img/step1.PNG',
        'static/img/step2.PNG',
        'static/img/step3.PNG',
        'static/img/step4.PNG',
        'static/img/step5.PNG',
        'static/img/step6.PNG',
        'static/img/step7.PNG'
    ],
    'depends': [
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view_import_purchase_order.xml',
        'views/view_import_purchase_order_wizard.xml',
        'views/view_sync_purchase_order_wizard.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [],
    },
    'assets': {
        'web.assets_backend': [
            'oe_import_purchase_order/static/src/js/tree_button.js',
        ],
        'web.assets_qweb': [
            'oe_import_purchase_order/static/src/xml/tree_button.xml',
        ],
    },

}