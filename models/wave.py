from openerp.osv import osv, fields


class StockPickingWave(osv.osv):
    _name = 'stock.picking.wave'
    _columns = {
	'name': fields.char('License Plate'),
    }
