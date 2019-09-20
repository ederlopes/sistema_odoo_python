# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Planilha(models.Model):

    _name = "susep.planilha"
    _description = "Tabs Planilha"

    name = fields.Char(
        string='Tab',
        required=True,
    )

    active = fields.Boolean(
        'Active',
        default=True
    )

    quadro_id = fields.Many2one(
        comodel_name='susep.quadro',
        string='Quadro',
    )

    mapeamento_ids = fields.Many2many(
        comodel_name='susep.mapeamento',
        string='Nome do campo',
    )

    planilha_campo_ids = fields.One2many(
        comodel_name='susep.planilha_campos',
        inverse_name='planilha_id',
        string='Campos'
    )

