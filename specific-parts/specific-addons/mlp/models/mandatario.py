# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Devedor(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name = 'mandatario'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete="cascade",
        required=True,
    )
