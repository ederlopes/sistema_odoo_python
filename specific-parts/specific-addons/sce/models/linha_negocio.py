# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LinhaNegocio(models.Model):
    _name = "linha.negocio"
    _rec_name = "sigla"
    _description = "Linha de negocio"

    name = fields.Char(
        string='Linha de Negócio',
        required=True,
    )

    sigla = fields.Char(
        string='Linha de Negócio',
        required=True,
    )

    active = fields.Boolean(
        string='Ativo',
    )

    status_linha_negocio_ids = fields.One2many(
        comodel_name='status.linha.negocio',
        inverse_name='linha_negocio_id',
        string='Status',
    )

    modalidade_ids = fields.One2many(
        comodel_name='modalidade',
        inverse_name='linha_negocio_id',
        string='Modalidades'
    )
