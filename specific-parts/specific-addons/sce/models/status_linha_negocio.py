# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StatusOrdem(models.Model):
    _name = "status.linha.negocio"
    _description = "Status Linha de Negócio"
    _order = 'ordem'

    ordem = fields.Integer(
        string='Ordem',
        required=True,
    )

    status_id = fields.Many2one(
        comodel_name='status',
    )

    linha_negocio_id = fields.Many2one(
        comodel_name='linha.negocio',
        string='Linha de negocio'
    )
