# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class QualityChecks(models.Model):
    _name = 'mrp.quality.checkpoint'
    _description = 'Quality Checkpoints'

    mrp_production_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Manufacturing Order',
    )
    name = fields.Char()
    move_id = fields.Many2one(
        comodel_name='stock.move',
        string='Component',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        related='move_id.product_id',
    )
    check_type = fields.Selection(
        selection=[
            ('comp_usage', 'Component Usage'),
        ],
        default='comp_usage',
    )
    tolerance = fields.Float(
        string='Tolerance Range',
    )
    measured_value = fields.Float()
    move_quantity = fields.Float(
        compute='_compute_move_qty',
    )
    state = fields.Selection(
        selection=[
            ('pass', 'Pass'),
            ('fail', 'Fail'),
        ],
        compute='_compute_state',
        store=True,
    )
    message = fields.Text(
        compute='_compute_state',
        store=True,
    )

    @api.depends('move_quantity', 'tolerance', 'measured_value')
    def _compute_state(self):
        for each in self:
            each.message = False
            if not each.measured_value:
                if not each.move_quantity:
                    each.state = 'pass'
                    continue
                each.state = False
                continue
            tol = each.tolerance or 0
            passed = abs(each.move_quantity - each.measured_value) <= tol
            if passed:
                each.state = 'pass'
            else:
                each.state = 'fail'
                each.message = 'The measured value is out of tolerance range'

    def _compute_move_qty(self):
        for each in self:
            each.move_quantity = each.move_id.quantity if each.move_id.picked else 0
        self._compute_state()
