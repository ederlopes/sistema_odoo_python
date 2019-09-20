# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Modalidade(models.Model):

    _name = "modalidade"
    _description = "Modalidade da linha de negocio"

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

    linha_negocio_id = fields.Many2one(
        comodel_name='linha.negocio',
        string='Linha de negocio'
    )

    tipo_financiamento_ids = fields.One2many(
        comodel_name='tipo.financiamento',
        inverse_name='modalidade_id',
        string='Tipo de financiamento'
    )
