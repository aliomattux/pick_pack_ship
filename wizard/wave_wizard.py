from openerp.osv import osv, fields
from datetime import datetime, timedelta

class StockPickingWaveWizard(osv.osv_memory):
    _name = 'stock.picking.wave.wizard'
    _columns = {
	'preset': fields.many2one('stock.picking.wave.preset', 'Preset'),
	'name': fields.char('Name'),
	'number_waves': fields.integer('Number of Waves to Generate'),
	'specify_items': fields.boolean('Specify Items'),
	'picking_type_id': fields.many2one('stock.picking.type', 'Warehouse'),
	'max_picks': fields.integer('Maximum number of picks/containers'),
	'max_units': fields.integer('Maximum number of units'),
	'specified_items': fields.many2many('product.product', 'stock_picking_wave_items_rel', 'wizard_id', 'product_id', 'Specified Items'),
	'max_items': fields.integer('Maximum number of items'),
	'from_date': fields.datetime('From Order Date'),
	'to_date': fields.datetime('To Order Date'),
	'availability_policy': fields.selection([('mixed', 'Mixed (Both Partial and Fully available orders)'), \
					('ready', 'Only fully comitted orders'), \
					('partial', 'Only partially available orders')]
	, 'Availability Policy', required=True),
    }


    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
	kanban_ids = context.get('active_ids', [])
	kanban = kanban_ids[0]
	res = {'picking_type_id': kanban,
		'availability_policy': 'ready',
		'number_waves': 1,
	}

	return res


    def wave_wizard_generator(self, cr, uid, ids, context=None):
	wizard = self.browse(cr, uid, ids[0])
	waves = self.find_waves(cr, uid, wizard)
	return self.pool.get('stock.picking.wave').create_waves(cr, uid, wizard.picking_type_id.id, waves)


    def find_waves(self, cr, uid, wizard):
	waves = {}
	for x in range(wizard.number_waves):
	    waves[x] = self.find_picks(cr, uid, wizard)

	return waves


    def prepare_picking_domain(self, cr, uid, wizard, context=None):
	domain = [('picking_type_id', '=', wizard.picking_type_id.id),
		('printed', '!=', True)
	]

	policy = wizard.availability_policy

	if policy == 'mixed':
	    domain.extend(['|',('state', 'in', ['assigned', 'partially_available']), ('pick_ahead', '=', True)])
	elif policy == 'ready':
	    domain.extend(['|',('state', '=', 'assigned'), ('pick_ahead', '=', True)])
	elif policy == 'partial':
	    domain.extend(['|',('state', '=', 'partially_available'), ('pick_ahead', '=', True)])

	if wizard.from_date:
	    domain.extend([('sale.date_order', '>', wizard.from_date)])

        if wizard.to_date:
	    date = datetime.strptime(wizard.to_date, '%Y-%m-%d %H:%M:%S')
	    to_date = date + timedelta(days=1)	    
            domain.extend([('sale.date_order', '<', to_date.strftime('%Y-%m-%d %H:%M:%S'))])

	return domain


    def search_parent_pickings(self, cr, uid, wizard, domain, context=None):
	if wizard.max_picks and wizard.max_picks > 0:
	    limit = wizard.max_picks
	else:
	    limit = False
	return self.pool.get('stock.picking').search(cr, uid, domain, limit=limit)


    def find_picks(self, cr, uid, wizard):
	domain = self.prepare_picking_domain(cr, uid, wizard)
	picking_ids = self.search_parent_pickings(cr, uid, wizard, domain)
	remaining_picks = self.filter_parent_picks(cr, uid, wizard, picking_ids)
	return remaining_picks


    def filter_parent_picks(self, cr, uid, wizard, picking_ids, context=None):

	if wizard.max_units < 1 and wizard.max_items < 1 or not picking_ids:
	    return picking_ids

	#doing direct sql for performance and because ORM cant do this
	base_query = "SELECT move.picking_id, COUNT(move.id) AS count_items," \
		" SUM(move.product_qty) AS number_units" \
		"\nFROM stock_move move" \

	#When using interpolation, you cant use % (tuple(ids),) because
	#if there is only 1 id then you will get WHERE id IN (1,)
	#Which is not valid syntax.
	#If you dont like this code, then provide a different example.
	#I wrote it this way because I dont know of any other way to have the same result
	#And have reasonable performance and no costly for loops

	if len(picking_ids) > 1:
	    where_sql = "\nWHERE move.picking_id IN %s" % (tuple(picking_ids),)
	else:
	    where_sql = "\nWHERE move.picking_id = %s" % picking_ids[0]

	if wizard.specify_items and wizard.specified_items:
	    item_ids = [product.id for product in wizard.specified_items]
	    if len(item_ids) > 1:
		where_sql += "\nAND move.product_id IN %s" % (tuple(item_ids),)
	    else:
		where_sql += "\nAND move.product_id = %s" % item_ids[0]
		
	group_sql = "\nGROUP BY picking_id"

	sql = base_query + where_sql + group_sql
	cr.execute(sql)
	picks = cr.dictfetchall()
	max_items = wizard.max_items
	max_units = wizard.max_units
	current_items = 0
	current_units = 0
	todo_picking_ids = []
	for pick in picks:
	    if max_units > 0:
		projected_units = pick['number_units'] + max_units
		if projected_units > max_units:
	            continue
		if projected_units == max_units:
		    break
            if max_items > 0:
                projected_items = pick['count_items'] + max_items
                if projected_items > max_items:
                    continue
                if projected_items == max_items:
                    break

	    current_items += pick['count_items']
	    current_units += pick['number_units']

	    todo_picking_ids.append(pick['picking_id'])

	self.pool.get('stock.picking').write(cr, uid, todo_picking_ids, \
		{'printed': True, 'printed_date': datetime.utcnow()}
	)

	return todo_picking_ids


class StockPickingWavePreset(osv.osv):
    _name = 'stock.picking.wave.preset'
    _columns = {
        'name': fields.char('Preset Name'),
	'number_waves': fields.integer('Number of Waves to Generate'),
        'max_picks': fields.integer('Maximum number of picks/containers'),
        'max_units': fields.integer('Maximum number of units'),
	'specified_items': fields.many2many('product.product', 'stock_picking_wave_items_rel', 'wizard_id', 'product_id', 'Specified Items'),
        'from_date': fields.datetime('From Order Date'),
        'to_date': fields.datetime('To Order Date'),
	'specify_items': fields.boolean('Specify Items'),
        'max_items': fields.integer('Maximum number of items'),
	'availability_policy': fields.selection([('mixed', 'Mixed (Both Partial and Fully available orders)'), \
					('ready', 'Only fully comitted orders'), \
					('partial', 'Only partially available orders')]
	, 'Availability Policy', required=True),
    }
