# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InstituicaoFinanceira(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name = 'instituicao.financeira'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete="cascade",
        required=True,
    )

    bank_id = fields.Many2one(
        comodel_name='res.bank',
        string='Instituição Financeira',
    )

    gecex_ids = fields.One2many(
        comodel_name='gecex',
        inverse_name='instituicao_financeira_id',
        string='Gecex',
    )

    agencia_ids = fields.One2many(
        comodel_name='agencia',
        inverse_name='instituicao_financeira_id',
        string='Agencias'
    )

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, '{} - {}'.
                        format(str(record.bank_id.bic), record.bank_id.name)))
        return res

