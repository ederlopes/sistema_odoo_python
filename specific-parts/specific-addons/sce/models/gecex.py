# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Gecex(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name = 'gecex'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete="cascade",
        required=True,
    )

    instituicao_financeira_id = fields.Many2one(
        comodel_name='instituicao.financeira',
        string='Instituição Financeira',
    )

    bank_ids = fields.One2many(
        comodel_name='agencia',
        inverse_name='gecex_id',
        string='Gecex',
    )
