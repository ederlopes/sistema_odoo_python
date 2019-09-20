# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Garantidor(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _description = "Garantidor"
    _name = 'garantidor'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete="cascade",
        required=True,
    )
