from openerp.osv import osv, fields


class SaleOrder(osv.osv):
    _inherit = 'sale.order'
    _columns = {
        'pick_ahead': fields.boolean('Pick Ahead'),
    }
