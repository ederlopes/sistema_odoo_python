# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OperacaoMercadoria(models.Model):
    _name = 'operacao.mercadoria'

    operacao_id = fields.Many2one(
        comodel_name='operacao',
        string='Operacao'
    )

    name = fields.Char(
        string='Mercadoria',
    )

    nu_ncm = fields.Char(
        string='NCM',
    )

    valor = fields.Float(
        digits=(15, 2),
        string='Valor',
    )

    nu_quantidade = fields.Integer(
        string='Quantidade',
    )
