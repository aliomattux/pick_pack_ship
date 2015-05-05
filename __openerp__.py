{
    'name': 'Pick Pack Ship',
    'version': '1.1',
    'author': 'Kyle Waid',
    'category': 'Sales Management',
    'depends': ['mage2odoo_operations', 'mage2odoo_picking_ticket'],
    'website': 'https://www.gcotech.com',
    'description': """ 
    """,
    'data': [
	'wizard/wave_wizard.xml',
	'data/wave_sequence.xml',
	'views/wave.xml',
	'views/stock.xml',
	'views/sale.xml',
	'report.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
