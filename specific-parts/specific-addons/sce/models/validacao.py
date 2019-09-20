# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Validacao(models.Model):
    _name = "validacao"
    _description = "Validação de atividades"

    active = fields.Boolean(
        string='Ativo',
    )

    name = fields.Char(
        string='Atividade a fazer',
        required=True,
    )

    url = fields.Char(
        string='Url do site a verificar',
        required=True,
    )

    linha_negocio_id = fields.Many2one(
        comodel_name='linha.negocio',
        string="Linha de Negocio",
    )
