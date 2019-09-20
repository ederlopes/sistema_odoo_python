# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning


class OperacaoMlpDecomposicaoPreco(models.Model):
    _name = "operacaomlp.depomposicao.preco"
    _description = "Decomposição do preco para operações MLP"

    decomposicao_preco_id = fields.Many2one(
        string='Descrição',
        comodel_name='decomposicao.preco',
    )

    decomposicao_localidade_id = fields.Many2one(
        string='Localidade',
        comodel_name='decomposicao.localidade',
    )

    valor = fields.Float(
        digits=(15, 2),
        string='Valor',
    )
