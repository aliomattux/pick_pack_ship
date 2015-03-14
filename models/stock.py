from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import time

class StockPickingType(osv.osv):
    _inherit = 'stock.picking.type'

    def _get_picking_count(self, cr, uid, ids, field_names, arg, context=None):
        obj = self.pool.get('stock.picking')
        domains = self._get_picking_count_domains()

        result = {}
        for field in domains:
            data = obj.read_group(cr, uid, domains[field] +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', ids)],
                ['picking_type_id'], ['picking_type_id'], context=context)
            count = dict(map(lambda x: (x['picking_type_id'] and x['picking_type_id'][0], x['picking_type_id_count']), data))
            for tid in ids:
                result.setdefault(tid, {})[field] = count.get(tid, 0)
        for tid in ids:
            if result[tid]['count_picking']:
                result[tid]['rate_picking_late'] = result[tid]['count_picking_late'] * 100 / result[tid]['count_picking']
                result[tid]['rate_picking_backorders'] = result[tid]['count_picking_backorders'] * 100 / result[tid]['count_picking']
            else:
                result[tid]['rate_picking_late'] = 0
                result[tid]['rate_picking_backorders'] = 0
        return result


    _columns = {
        'count_print': fields.function(_get_picking_count,
                type='integer', multi='_get_picking_count'),
        'count_ship_ready': fields.function(_get_picking_count,
                type='integer', multi='_get_picking_count'),
    }


    def _get_picking_count_domains(self, context=False):
        domains = super(StockPickingType, self)._get_picking_count_domains(context=context)
	domains.update({
	    'count_print': [('state', 'in', ('assigned', 'partially_available')), ('printed', '=', False)],
	    'count_ship_ready': [('state', 'in', ('assigned', 'partially_available')), ('printed', '=', True)],
	})

	return domains
