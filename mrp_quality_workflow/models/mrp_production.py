# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Production(models.Model):
    _inherit = 'mrp.production'

    quality_check_ids = fields.One2many(
        comodel_name='mrp.quality.checkpoint',
        inverse_name='mrp_production_id',
        string='Quality Checks',
    )
    state = fields.Selection(
        selection_add=[
            ('on_hold', 'On Hold'),
        ],
    )

    # * ================ Public methods ================
    def action_generate_quality_checks(self):
        if self._context.get('restart_quality_check'):
            self._compute_state()
        self._generate_quality_checks()

    def action_confirm(self):
        for mo in self:
            mo._generate_quality_checks()
        return super().action_confirm()

    # * ================ Private methods ================
    def _generate_quality_checks(self):
        self.ensure_one()
        self.write({
            'quality_check_ids': [
                fields.Command.clear()
            ] + [
                fields.Command.create({
                    'move_id': raw.id,
                })
                for raw in self.move_raw_ids
            ]
        })

    def _button_mark_done_sanity_checks(self):
        super()._button_mark_done_sanity_checks()
        for mo in self:
            quality_checks = mo.quality_check_ids
            if not quality_checks:
                continue
            if False in quality_checks.mapped('state'):
                raise ValidationError(
                    _(f'Cannot Validate {mo.name}: Skipped some/all Quality Checks.'))

    def _compute_state(self):
        super(Production, self)._compute_state()
        restart_check = self._context.get('restart_quality_check')
        for mo in self:
            quality_checks = mo.quality_check_ids
            if not quality_checks:
                continue
            if restart_check:
                mo.state = 'confirmed'
            elif mo.state == 'done' and 'fail' in quality_checks.mapped('state'):
                mo.state = 'on_hold'
