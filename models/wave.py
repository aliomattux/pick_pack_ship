from openerp.osv import osv, fields
from datetime import datetime

class StockPickingWave(osv.osv):
    _name = 'stock.picking.wave'

    def _picks_count(self, cr, uid, ids, field_name, arg, context=None):
        if not ids:
            return {}
#        cr.execute("select transaction, count(id) from stock_move where transaction in %s group by transaction",(tuple(ids),))
#        res = dict(cr.fetchall())
        return res

    _columns = {
	'name': fields.char('License Plate'),
	'picking_type_id': fields.many2one('stock.picking.type', 'Warehouse'),
	'state': fields.selection([('new', 'New'), ('printed', 'Printed')]
	, 'Status', required=True),
	'date': fields.datetime('Created On'),
	'last_print_date': fields.datetime('Last Printed Date'),
#	'picks_count': fields.function(_picks_count, method=True, type="integer", store=True, string="# Picks"),
	'picks': fields.one2many('stock.picking.wave.container', 'wave', 'Picks', readonly=True),
    }


    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.wave') or '/'

        new_id = super(StockPickingWave, self).create(cr, uid, vals, context=context)
        return new_id


    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
	'state': 'new',
    }


    def button_print_wave(self, cr, uid, ids, context=None):
	return self.serve_this_wave(cr, uid, ids)


    def button_print_picks(self, cr, uid, ids, context=None):
	wave = self.browse(cr, uid, ids[0])
	picks = wave.picks
        datas = {'ids' : [container.pick.id for container in picks],
		'model': 'stock.picking',
		'form': {}
	}
        return {
            'type': 'ir.actions.report.xml',
            'report_name':'pack.slip',
            'datas' : datas,
       }


    def serve_this_wave(self, cr, uid, wave_ids, context=None):
	if not context:
	    context = {}

        datas = {'ids' : wave_ids}
        datas['form'] = {}
        return {
            'type': 'ir.actions.report.xml',
            'report_name':'picking.wave',
            'datas' : datas,
       }


    def create_waves(self, cr, uid, picking_type_id, waves, context=None):
	print 'waves', waves
	for k, v in waves.items():
	    wave = self.create_wave(cr, uid, picking_type_id, v)

	return True


    def create_wave(self, cr, uid, picking_type_id, picking_ids, context=None):
	container = 1
	wave_lines = []
	for picking_id in picking_ids:
	    wave_lines.append((0, 0, {'pick': picking_id,
			'container': container,
	    }))
	    container += 1

	vals = {'picking_type_id': picking_type_id,
		'date': datetime.utcnow(),
		'picks': wave_lines
	}

	wave_id = self.create(cr, uid, vals)
	return True


class StockPickingWaveContainer(osv.osv):
    _name = 'stock.picking.wave.container'
    _rec_name = 'container'
    _columns = {
	'container': fields.char('Container', required=True),
	'last_print_date': fields.related('container', 'last_date_printed', string="Last Date Printed", type="datetime"),
	'wave': fields.many2one('stock.picking.wave', 'Wave', ondelete='cascade', select=True, require=True),
	'pick': fields.many2one('stock.picking', 'Pick', ondelete='cascade', select=True, required=True),
	'pick_state': fields.related('pick', 'state', string="State", type="char"),
    }
