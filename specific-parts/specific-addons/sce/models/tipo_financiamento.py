# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoFinanciamento(models.Model):

    _name = "tipo.financiamento"
    _description = "Tipo financiamento da modalidade"

    name = fields.Char(
        string='Nome',
        required=True,
    )

    sigla = fields.Char(
        string='Sigla',
    )

    active = fields.Boolean(
        string='Ativo',
    )

    modalidade_id = fields.Many2one(
        comodel_name='modalidade',
        string='Modalidade'
    )
