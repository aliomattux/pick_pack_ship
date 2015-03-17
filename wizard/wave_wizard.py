from openerp.osv import osv, fields


class StockPickingWaveWizard(osv.osv_memory):
    _name = 'stock.picking.wave.wizard'
    _columns = {
	'name': fields.char('Name'),
	'picking_type_id': fields.many2one('stock.picking.type', 'Warehouse'),
	'max_picks': fields.integer('Maximum number of picks/containers'),
	'max_units': fields.integer('Maximum number of units'),
	'max_items': fields.integer('Maximum number of items'),
	'availability_policy': fields.selection([('mixed', 'Mixed (Both Partial and Fully available)'), \
					('ready', 'Only Fully available picks'), \
					('partial', 'Only Partially available picks')]
	, 'Availability Policy', required=True),
    }


    _defaults = {
	'availability_policy': 'mixed',
    }


    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
	kanban_ids = context.get('active_ids', [])
	kanban = kanban_ids[0]
	res = {'picking_type_id': kanban}

	return res


    def create_wave(self, cr, uid, ids, context=None):
	wizard = self.browse(cr, uid, ids[0])
	picks = self.find_picks(cr, uid, wizard)
	print picks
	return self.pool.get('stock.picking.wave').create_wave(cr, uid, wizard.picking_type_id.id, picks)
	return True


    def prepare_picking_domain(self, cr, uid, wizard, context=None):
	domain = [('picking_type_id', '=', wizard.picking_type_id.id)]

	policy = wizard.availability_policy

	if policy == 'mixed':
	    domain.append(('state', 'in', ['assigned', 'partially_available']))
	elif policy == 'ready':
	    domain.append(('state', '=', 'assigned'))
	elif policy == 'partial':
	    domain.append(('state', '=', 'partially_available'))

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

	if wizard.max_units < 1 and wizard.max_items < 1:
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

	return todo_picking_ids
