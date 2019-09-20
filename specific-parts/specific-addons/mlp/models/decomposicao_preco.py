# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DecomposicaoPreco(models.Model):

    _name = "decomposicao.preco"
    _description = "Decomposição do preço da Operação"

    name = fields.Char(
        string='Nome',
        required=True,
    )

    active = fields.Boolean(
        string='Ativo',
    )

