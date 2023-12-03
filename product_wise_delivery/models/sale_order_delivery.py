from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    # def action_confirm(self):
    #     print(self.picking_ids, '======')
    #     res = super(SaleOrderInherit, self).action_confirm()
    #     print(res, '------------', self.picking_ids)

        # return res

    def _action_confirm(self):
        print(self.picking_ids, 'before')


        product_qty = {}
        for line in self.order_line:
            qty = product_qty.get(line.product_id.id, 0)
            product_qty[line.product_id.id] = qty + line.product_uom_qty

        # products = []
        delivery_ids = []
        picking_type = self.env['stock.picking.type'].search([('name', '=', 'Delivery Orders'), ('code', '=', 'outgoing')])
        location_id = self.env['stock.location'].search([('name', '=', 'Stock')])
        for product_id, quantity in product_qty.items():
            # if line.product_template_id.id not in products:
            #     products.append(line.product_template_id.id)
            delivery_id =   self.env['stock.picking'].create({
                'partner_id':self.partner_id.id,
                'picking_type_id':picking_type.id,
                'location_id': location_id.id,
                'origin':self.name,
                'location_dest_id':self.partner_id.property_stock_customer.id,
                'move_ids':[(0,0, {'name':self.name,'product_id': product_id,'product_uom_qty': quantity,'location_id':location_id.id,'location_dest_id':self.partner_id.property_stock_customer.id})]
                })
            delivery_id.state = 'assigned'
            delivery_ids.append(delivery_id.id)
        #     self.env['stock.move'].create({
        #     'name':delivery_id.name,
        #     'product_id': product_id,
        #     'product_uom_qty': quantity,
        #     'picking_id': delivery_id.id,
        #     'location_id':location_id.id,
        #     'location_dest_id':self.partner_id.property_stock_customer.id
        # })

        res = super(SaleOrderInherit, self)._action_confirm()
        self.picking_ids = delivery_ids
        print(self.picking_ids, 'after')
        return res


# class SaleOrderLineInherit(models.Model):
#     _inherit = "sale.order.line"

    # def _action_launch_stock_rule(self,previous_product_uom_qty=False):
    #     print( '////////////////=========/', print(self.order_id.picking_ids))
    #     self.order_id.picking_ids = [4, 21]
    #     res = super(SaleOrderInherit, self)._action_launch_stock_rule()
    #     print(res, '=========/', print(self.order_id.picking_ids))

    #     return res