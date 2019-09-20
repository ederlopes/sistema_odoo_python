# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning


class Agencia(models.Model):
    _name = "agencia"
    _rec_name = 'agencia'

    agencia = fields.Char(
        string='Agencia',
    )

    gecex_id = fields.Many2one(
        comodel_name='gecex',
        string='Gecex',
    )

    instituicao_financeira_id = fields.Many2one(
        comodel_name='instituicao.financeira',
        string='Instituicao Financeira',
    )

    cpf_cnpj = fields.Char(
        string='CNPJ',
    )

    insc_estadual = fields.Char(
        string='Inscrição Estatudal',
    )

    cargo = fields.Char(
        string='Cargo',
    )

    active = fields.Boolean(
        string='Status',
        default=True
    )
