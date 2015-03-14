from openerp.osv import osv, fields



class StockPickingWaveWizard(osv.osv_memory):
    _name = 'stock.picking.wave.wizard'
    _columns = {
	'name': fields.char('Name'),
    }
