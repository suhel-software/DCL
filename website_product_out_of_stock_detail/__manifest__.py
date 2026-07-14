# -*- coding: utf-8 -*-
{
    'name': 'Website Product Out of Stock Detail',
    'version': '16.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Display out-of-stock message on product detail page even without variant selection.',
    'description': """
        Displays the "Out of Stock" message on the website product detail page on load
        if the product or its default variant is out of stock.
    """,
    'author': 'Antigravity',
    'depends': ['website_sale_stock'],
    'data': [
        'views/website_sale_stock_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_product_out_of_stock_detail/static/src/css/out_of_stock.scss',
            'website_product_out_of_stock_detail/static/src/js/website_sale.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
