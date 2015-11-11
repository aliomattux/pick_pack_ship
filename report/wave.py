import time
from datetime import datetime
from openerp.report import report_sxw
from pprint import pprint as pp
from openerp.tools.translate import _
from tzlocal import get_localzone

BLANK =  {
          'qty_order': ' ',
          'qty_ship': ' ',
	  'location': ' ',
          'sku': ' ',
          'description': ' ',
          'description2': ' ',
}

class PickWaveReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(PickWaveReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'paginate_items': self._paginate_items, 
				  'get_date_created': self._get_date_created,
				  'current_date': self._current_date,
				  'mark_printed': self._mark_printed
	})

    def _current_date(self):
	date = datetime.utcnow()
	tz = get_localzone()
	t = tz.localize(date)
	return datetime.strftime(date, '%m/%d/%Y')


    def _get_date_created(self, picking):
        if picking.create_date and picking.create_date != 'False':
            date_obj = datetime.strptime(picking.create_date, '%Y-%m-%d %H:%M:%S')
            tz = get_localzone()
            dt = tz.localize(date_obj)
            return datetime.strftime(dt, '%m/%d/%Y')

        return ' '


    def get_backorder_qty(self, move):
	cr = self.cr
	query = """SELECT SUM(product_qty) AS "qty" FROM stock_move WHERE split_from = %s AND state != 'done'""" % move.id
	cr.execute(query)
	results = cr.fetchone()
	if results and results[0]:
	    return int(results[0])
	else:
	    return 0


    def line_val_dict(self, container, product, move):
#	if move.picking_id.state == 'done':
	qty = int(move.product_qty)
#	else:
	    #This can be toggled for use with displaying actual posted data vs future data
#	    qty = int(move.product_qty)

        return {
                'qty_order': int(move.procurement_id.product_qty),
                'qty_ship': qty,
                'sku': product.default_code or '',
                'container': container.container if container else ' ',
                'location': move.location_id.name or ' ',
                'description': product.name or '',
                'description2': product.name or '',
	}


    def prepare_line_val(self, wave, container, product, move):
	cr = self.cr
	uid = self.uid

	items = []

	items.append(self.line_val_dict(container, product, move))

	return items


    def _get_components_list(self, wave, container, line):
	result = []
	for component in line.item.components:
	    result.extend(self.prepare_line_val(wave, container, component.item, component.qty * line.qty))

	return result


    def _process_lines(self, cr, uid, wave, container, lines):
	result = []
        for line in lines:
	    result.extend(self.prepare_line_val(wave, container, line.product_id, line))

#	result.extend(self.show_backorder_lines(cr, uid, line))
	return result
#	return sorted(result, key=lambda id: id['prime_location'])


    def batch_picking_lines(self, cr, uid, picks, wave):
	master_dict = {}
        for container in picks:
	    picking = container.pick
	    for move in picking.move_lines:
		product = move.product_id
		if master_dict.get(product.id):
		    master_dict[product.id]['qty_ship'] += move.product_qty
		else:
		    master_dict[product.id] = self.line_val_dict(False, product, move)

	lines = []
	for k, v in master_dict.items():
	    lines.append(v)

	return lines


    def _paginate_items(self, picks, wave):
	cr = self.cr
	uid = self.uid
	if wave.not_containerized:
	    processed_lines = self.batch_picking_lines(cr, uid, picks, wave)

	else:
	    processed_lines = []

	    for container in picks:
	        pick = container.pick
	        pick_lines = [move for move in pick.move_lines]
	        lines = self._process_lines(cr, uid, wave, container, pick_lines)
	        processed_lines.extend(lines)
	    
        items_per_page = 15
        result = []
        linecount = len(processed_lines)
        myrange = range(0,linecount)
        #myarrays = myrange[i:i+items_per_page]

        pages = [ myrange[i:i+items_per_page] for i in range(0,linecount,items_per_page) ]
        for page in pages:
            pagelist = []
            for order in page:
                pagelist.append(processed_lines[order])
	    if len(pagelist) != 13:
		for x in range(13 - len(pagelist)):
		    pagelist.append(BLANK)
            result.append(pagelist)
        return result


    def _mark_printed(self, pickings):
        cr = self.cr
        uid = self.uid

        picking_obj = self.pool.get('stock.picking')
	print_obj = self.pool.get('print.history')

        for picking in pickings:
 #           print_obj.create(cr, uid, {'picking': picking.id, 'status': 'success', 'user_id': uid, 'date': datetime.utcnow()})
	    picking_obj.write(cr, 1, picking.id, {'printed': True, 'printed_date': datetime.utcnow()})
		
        return True


report_sxw.report_sxw('report.picking.wave',
                      'stock.picking.wave',
                      'addons/pick_pack_ship/report/wave.mako',
                      parser=PickWaveReport)
